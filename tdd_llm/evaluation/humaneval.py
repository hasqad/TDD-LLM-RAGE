"""
HumanEval benchmark evaluation.

Downloads the HumanEval dataset and evaluates each pipeline's pass@1 score.
Each HumanEval problem ships with its own ground-truth test function,
so no LLM-generated tests are used — results are objective.
"""

import gzip
import json
import os
import shutil
import subprocess
import sys
import sysconfig
import tempfile
import urllib.request
from pathlib import Path

def _find_venv_site_packages() -> str | None:
    for parent in Path(__file__).resolve().parents:
        for name in ("venv", ".venv", "env"):
            lib = parent / name / "lib"
            if lib.is_dir():
                for pyver in lib.iterdir():
                    sp = pyver / "site-packages"
                    if sp.is_dir():
                        return str(sp)
    return None

_VENV_SITE_PACKAGES: str | None = _find_venv_site_packages()
_PYTHON_CMD: str = sys.executable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

HUMANEVAL_URL = (
    "https://github.com/openai/human-eval/raw/master/data/HumanEval.jsonl.gz"
)
CACHE_PATH = Path(__file__).parent.parent.parent / "data" / "HumanEval.jsonl.gz"


# ---------------------------------------------------------------------------
# Dataset loading
# ---------------------------------------------------------------------------

def _download_humaneval() -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"[HumanEval] Downloading dataset from GitHub...")
    urllib.request.urlretrieve(HUMANEVAL_URL, CACHE_PATH)
    print(f"[HumanEval] Saved to {CACHE_PATH}")


def load_problems(n: Optional[int] = None, offset: int = 0) -> list[dict]:
    """Load HumanEval problems. Downloads on first use.

    Args:
        n: number of problems to return (None = all)
        offset: skip the first `offset` problems (use higher-indexed, harder problems)
    """
    if not CACHE_PATH.exists():
        _download_humaneval()

    problems = []
    with gzip.open(CACHE_PATH, "rt", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                problems.append(json.loads(line))

    problems = problems[offset:]
    if n is not None:
        problems = problems[:n]
    return problems


# ---------------------------------------------------------------------------
# Single-problem evaluation
# ---------------------------------------------------------------------------

def _run_humaneval_test(solution_code: str, problem: dict, timeout: int = 10) -> bool:
    """
    Run one HumanEval problem's check() against the generated solution.
    Returns True if all assertions pass.
    """
    entry = problem["entry_point"]
    test_code = problem["test"]  # defines check(candidate)

    script = (
        f"{solution_code}\n\n"
        f"{test_code}\n\n"
        f"check({entry})\n"
    )

    with tempfile.NamedTemporaryFile(
        suffix=".py", mode="w", encoding="utf-8", delete=False
    ) as f:
        f.write(script)
        tmp_path = f.name

    try:
        env = os.environ.copy()
        if _VENV_SITE_PACKAGES:
            existing = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = (
                _VENV_SITE_PACKAGES + os.pathsep + existing if existing
                else _VENV_SITE_PACKAGES
            )
        proc = subprocess.run(
            [_PYTHON_CMD, tmp_path],
            capture_output=True, text=True, timeout=timeout, env=env,
        )
        return proc.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    finally:
        os.unlink(tmp_path)


# ---------------------------------------------------------------------------
# Pipeline evaluation
# ---------------------------------------------------------------------------

@dataclass
class HumanEvalResult:
    pipeline: str
    problems_total: int = 0
    problems_passed: int = 0
    pass_at_1: float = 0.0
    per_problem: list[dict] = field(default_factory=list)


def evaluate_pipeline(
    pipeline_name: str,
    pipeline,
    problems: list[dict],
    samples_per_problem: int = 1,
    seed_offset: int = 0,
) -> HumanEvalResult:
    """
    Run a pipeline on all HumanEval problems and return pass@1.

    For each problem:
    - Uses the HumanEval prompt (function signature + docstring) as the task
    - Generates `samples_per_problem` code samples
    - Passes if ANY sample passes the ground-truth check()

    The iterative pipeline generates LLM tests from the docstring and uses
    test feedback to iteratively improve its code (up to max_iterations).
    Batch and notdd pipelines make a single code generation attempt each.
    """
    from ..evaluation.pass_at_k import compute_pass_at_k
    from ..pipelines.iterative_pipeline import IterativePipeline

    result = HumanEvalResult(pipeline=pipeline_name, problems_total=len(problems))
    passed_flags = []

    for i, problem in enumerate(problems):
        task_id = problem["task_id"]
        prompt = problem["prompt"]          # function sig + docstring

        # Build a minimal task dict compatible with pipeline.run_sample
        task = {
            "title": task_id,
            "function_signature": _extract_signature(prompt),
            "description": prompt,
            "constraints": "",
            "example_inputs": "",
            "expected_outputs": "",
        }

        # Iterative pipeline: build a mini test suite from the docstring >>> examples.
        # These are ground-truth examples from the spec — always correct, no hallucination.
        # This gives iterative real feedback to iterate on while batch/notdd get none.
        fn_name = task["function_signature"].split("(")[0].replace("def ", "").strip()
        if isinstance(pipeline, IterativePipeline):
            tests_for_feedback = _doctest_to_pytest(prompt, fn_name)
        else:
            tests_for_feedback = ""

        sample_passed = False
        for s in range(samples_per_problem):
            seed = (i + 1) * 1000 + seed_offset + s * 100
            try:
                sample = pipeline.run_sample(task, tests_code=tests_for_feedback, seed=seed)
                if sample.code:
                    passed = _run_humaneval_test(sample.code, problem)
                    if passed:
                        sample_passed = True
                        break
            except Exception:
                pass

        passed_flags.append(sample_passed)
        status = "PASS" if sample_passed else "FAIL"
        print(f"  [{pipeline_name}] {task_id} ... {status}")

        result.per_problem.append({
            "task_id": task_id,
            "passed": sample_passed,
        })

    pak = compute_pass_at_k(passed_flags)
    result.problems_passed = pak.c
    result.pass_at_1 = round(pak.pass_at_1, 4)
    return result


def _extract_signature(prompt: str) -> str:
    """Extract the def line from a HumanEval prompt."""
    for line in prompt.splitlines():
        if line.strip().startswith("def "):
            return line.strip()
    return "def solution():"


def _doctest_to_pytest(prompt: str, fn_name: str) -> str:
    """
    Convert HumanEval docstring >>> examples into a minimal pytest test suite.

    These examples are ground-truth (from the spec), so they are always correct.
    Using them as iterative feedback avoids LLM test hallucination.
    """
    import re
    lines = prompt.splitlines()
    tests: list[str] = []
    idx = 1
    i = 0
    while i < len(lines):
        stripped = lines[i].strip()
        if stripped.startswith(">>>"):
            call = stripped[3:].strip()
            if i + 1 < len(lines):
                nxt = lines[i + 1].strip()
                if nxt and not nxt.startswith(">>>"):
                    tests.append(
                        f"def test_example_{idx}():\n"
                        f"    assert {call} == {nxt}\n"
                    )
                    idx += 1
                    i += 2
                    continue
        i += 1

    if not tests:
        return ""
    return f"from solution import {fn_name}\n\n" + "\n".join(tests)
