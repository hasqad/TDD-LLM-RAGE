#!/usr/bin/env python3
"""
Show all historical runs from the runs/ directory.
These were saved by run_experiment.py and are NOT in benchmark_results.jsonl.
"""

import json
import re
import sys
from pathlib import Path

RUNS_DIR = Path(__file__).parent / "runs"


def parse_run_dir(run_dir: Path) -> dict | None:
    metrics_file = run_dir / "metrics.json"
    if not metrics_file.exists():
        return None

    # Parse directory name: run_YYYYMMDD_HHMMSS_task{N}_{pipeline}_{model}_seed{S}
    name = run_dir.name
    m = re.match(
        r"run_(\d{8})_(\d{6})_task(\d+)_(iterative|batch|notdd)_(.+)_seed(\d+)$",
        name,
    )
    if not m:
        return None

    date, time_, task_num, pipeline, model, seed = m.groups()
    model = model.replace("_", ".")  # restore dots in model names

    # Read task title from query.txt
    task_title = ""
    query_file = run_dir / "query.txt"
    if query_file.exists():
        first_line = query_file.read_text().strip().splitlines()[0]
        task_title = first_line.replace("Title:", "").strip()

    metrics = json.loads(metrics_file.read_text())

    return {
        "date": f"{date[:4]}-{date[4:6]}-{date[6:]} {time_[:2]}:{time_[2:4]}:{time_[4:]}",
        "task_num": int(task_num),
        "task_title": task_title,
        "pipeline": pipeline,
        "model": model,
        "seed": int(seed),
        **metrics,
    }


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "summary"

    runs = []
    for d in sorted(RUNS_DIR.iterdir()):
        if d.is_dir():
            r = parse_run_dir(d)
            if r:
                runs.append(r)

    if not runs:
        print("No runs found.")
        return

    print(f"Total individual pipeline runs: {len(runs)}\n")

    if mode == "all":
        # Print every run
        print(f"{'Date':<20} {'Task':<30} {'Pipeline':<12} {'Model':<22} {'Seed':>5} "
              f"{'pass@1':>7} {'pass@5':>7} {'MutScore':>9} {'Attempts':>9}")
        print("-" * 125)
        for r in runs:
            print(
                f"{r['date']:<20} {r['task_title'][:29]:<30} {r['pipeline']:<12} "
                f"{r['model'][:21]:<22} {r['seed']:>5} "
                f"{r.get('pass_at_1', 0)*100:>6.1f}% "
                f"{r.get('pass_at_5', 0)*100:>6.1f}% "
                f"{r.get('mutation_score', 0)*100:>8.1f}% "
                f"{r.get('avg_attempts', 0):>9.1f}"
            )

    elif mode == "model":
        # Summary grouped by model + pipeline
        from collections import defaultdict
        groups = defaultdict(list)
        for r in runs:
            groups[(r["model"], r["pipeline"])].append(r)

        print(f"{'Model':<24} {'Pipeline':<12} {'Runs':>5} {'pass@1':>7} {'pass@5':>7} "
              f"{'MutScore':>9} {'CC':>6} {'LOC':>6} {'Attempts':>9}")
        print("-" * 90)

        for (model, pipeline) in sorted(groups):
            g = groups[(model, pipeline)]
            n = len(g)
            avg = lambda k: sum(r.get(k, 0) for r in g) / n
            print(
                f"{model[:23]:<24} {pipeline:<12} {n:>5} "
                f"{avg('pass_at_1')*100:>6.1f}% "
                f"{avg('pass_at_5')*100:>6.1f}% "
                f"{avg('mutation_score')*100:>8.1f}% "
                f"{avg('avg_cyclomatic_complexity'):>6.1f} "
                f"{avg('avg_lines_of_code'):>6.1f} "
                f"{avg('avg_attempts'):>9.1f}"
            )

    else:
        # Default: summary grouped by pipeline only
        from collections import defaultdict
        groups = defaultdict(list)
        for r in runs:
            groups[r["pipeline"]].append(r)

        print(f"{'Pipeline':<12} {'Runs':>5} {'pass@1':>7} {'pass@5':>7} "
              f"{'MutScore':>9} {'CC':>6} {'LOC':>6} {'Attempts':>9}")
        print("-" * 65)

        for pipeline in ["iterative", "batch", "notdd"]:
            g = groups.get(pipeline, [])
            if not g:
                continue
            n = len(g)
            avg = lambda k: sum(r.get(k, 0) for r in g) / n
            print(
                f"{pipeline:<12} {n:>5} "
                f"{avg('pass_at_1')*100:>6.1f}% "
                f"{avg('pass_at_5')*100:>6.1f}% "
                f"{avg('mutation_score')*100:>8.1f}% "
                f"{avg('avg_cyclomatic_complexity'):>6.1f} "
                f"{avg('avg_lines_of_code'):>6.1f} "
                f"{avg('avg_attempts'):>9.1f}"
            )

    print(f"\nTip: run with 'model' or 'all' argument for more detail:")
    print(f"  python3 show_all_runs.py model")
    print(f"  python3 show_all_runs.py all")


if __name__ == "__main__":
    main()
