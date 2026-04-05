"""
Run directory management — saves all experiment artifacts to disk.
"""

import json
import re
from datetime import datetime
from pathlib import Path

RUNS_DIR = Path(__file__).parent.parent.parent / "runs"


def make_run_dir(task_id: int, model: str, pipeline: str, seed: int) -> Path:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_safe = re.sub(r"[^a-zA-Z0-9_-]", "_", model)
    name = f"run_{ts}_task{task_id}_{pipeline}_{model_safe}_seed{seed}"
    path = RUNS_DIR / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_text(path: Path, filename: str, content: str) -> Path:
    target = path / filename
    target.write_text(content, encoding="utf-8")
    return target


def save_json(path: Path, filename: str, data: dict) -> Path:
    target = path / filename
    target.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return target


def save_run_artifacts(
    run_dir: Path,
    task_description: str,
    pipeline: str,
    tests_code: str,
    samples: list[dict],   # list of {index, seed, code, passed, ...}
    metrics: dict,
) -> None:
    """
    Saves:
      query.txt
      {pipeline}_tests.py
      metrics.json
      samples/
        sample_000/
          solution.py
          result.json
          iterations/   (iterative only)
    """
    save_text(run_dir, "query.txt", task_description)

    if tests_code:
        save_text(run_dir, f"{pipeline}_tests.py", tests_code)

    save_json(run_dir, "metrics.json", metrics)

    samples_dir = run_dir / "samples"
    samples_dir.mkdir(exist_ok=True)

    for s in samples:
        idx = s.get("index", 0)
        sample_dir = samples_dir / f"sample_{idx:03d}"
        sample_dir.mkdir(exist_ok=True)

        if s.get("code"):
            save_text(sample_dir, "solution.py", s["code"])

        result_data = {k: v for k, v in s.items() if k != "code" and k != "iterations"}
        save_json(sample_dir, "result.json", result_data)

        if s.get("iterations"):
            iter_dir = sample_dir / "iterations"
            iter_dir.mkdir(exist_ok=True)
            for it in s["iterations"]:
                save_json(iter_dir, f"iteration_{it['attempt']:03d}.json", it)
