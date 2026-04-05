"""
Iterative TDD pipeline — for one sample.
Generates tests, then iterates on code until tests pass or limit reached.
"""

import time
from dataclasses import dataclass, field
from typing import Optional

from ..utils.ollama_client import OllamaClient, extract_python_code
from ..prompts.code_prompts import (
    TEST_GENERATION_SYSTEM, TEST_GENERATION_PROMPT,
    CODE_GENERATION_SYSTEM, CODE_GENERATION_PROMPT,
    ITERATIVE_FEEDBACK_PROMPT,
)
from ..evaluation.test_runner import run_tests, TestResult

MAX_ITERATIONS = 5


@dataclass
class SampleResult:
    """Result for a single sample (one pipeline execution)."""
    code: str = ""
    tests_code: str = ""
    test_result: Optional[TestResult] = None
    iterations: list[dict] = field(default_factory=list)
    total_attempts: int = 0
    syntax_errors: int = 0
    passed: bool = False
    run_time: float = 0.0
    error: str = ""


class IterativePipeline:
    def __init__(self, client: OllamaClient, max_iterations: int = MAX_ITERATIONS):
        self.client = client
        self.max_iterations = max_iterations

    def generate_tests(self, task: dict, seed: int) -> str:
        """Generate tests once — shared across all samples for this pipeline."""
        fn_name = self._fn_name(task["function_signature"])
        prompt = TEST_GENERATION_PROMPT.format(
            task_description=self._description(task),
            function_signature=task["function_signature"],
            function_name=fn_name,
            example_inputs=task.get("example_inputs", ""),
            expected_outputs=task.get("expected_outputs", ""),
        )
        raw = self.client.generate(
            prompt=prompt, system=TEST_GENERATION_SYSTEM,
            temperature=0.2, seed=seed,
        )
        return extract_python_code(raw)

    def run_sample(self, task: dict, tests_code: str, seed: int) -> SampleResult:
        """
        Run one sample: generate code iteratively until tests pass.
        tests_code is shared (generated once per run, not per sample).
        seed controls this sample's LLM calls.
        """
        result = SampleResult(tests_code=tests_code)
        start = time.time()
        description = self._description(task)
        previous_code = ""
        feedback = ""
        code = ""

        # Without tests there is no feedback signal — a single generation is best.
        has_tests = bool(tests_code and tests_code.strip())
        max_attempts = self.max_iterations if has_tests else 1

        # Track the best code seen across iterations (by pass rate, then by attempt order).
        best_code = ""
        best_pass_rate = -1.0

        for attempt in range(1, max_attempts + 1):
            result.total_attempts = attempt

            if attempt == 1:
                prompt = CODE_GENERATION_PROMPT.format(
                    task_description=description,
                    function_signature=task["function_signature"],
                    constraints=task.get("constraints", ""),
                    example_inputs=task.get("example_inputs", ""),
                    expected_outputs=task.get("expected_outputs", ""),
                )
            else:
                prompt = ITERATIVE_FEEDBACK_PROMPT.format(
                    task_description=description,
                    function_signature=task["function_signature"],
                    previous_code=previous_code,
                    test_output=feedback,
                    attempt=attempt,
                )

            raw = self.client.generate(
                prompt=prompt, system=CODE_GENERATION_SYSTEM,
                temperature=0.5, seed=seed + attempt - 1,
            )
            code = extract_python_code(raw)

            syntax_err = ""
            try:
                compile(code, "solution.py", "exec")
            except SyntaxError as e:
                syntax_err = str(e)
                result.syntax_errors += 1

            test_result = run_tests(code, tests_code)

            result.iterations.append({
                "attempt": attempt,
                "code": code,
                "syntax_error": syntax_err,
                "tests_passed": test_result.passed,
                "tests_total": test_result.total,
                "output": test_result.output[:2000],
            })

            # Keep the best code seen (most tests passed).
            if test_result.pass_rate > best_pass_rate:
                best_pass_rate = test_result.pass_rate
                best_code = code

            if test_result.all_passed:
                result.code = code
                result.test_result = test_result
                result.passed = True
                break

            feedback = test_result.output[:3000]
            previous_code = code
        else:
            # Return the best code seen, not the last (which may have regressed).
            result.code = best_code or code
            result.test_result = run_tests(result.code, tests_code)
            result.passed = result.test_result.all_passed

        result.run_time = time.time() - start
        return result

    def _fn_name(self, signature: str) -> str:
        import re
        m = re.search(r"def\s+(\w+)", signature)
        return m.group(1) if m else "solution"

    def _description(self, task: dict) -> str:
        return (
            f"{task.get('description', '')}\n\n"
            f"Constraints: {task.get('constraints', '')}\n"
            f"Example inputs: {task.get('example_inputs', '')}\n"
            f"Expected outputs: {task.get('expected_outputs', '')}"
        )
