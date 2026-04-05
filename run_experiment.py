#!/usr/bin/env python3
"""
TDD-LLM Experiment Framework — CLI

python run_experiment.py \\
    --task_source known \\
    --model deepseek-coder:6.7b \\
    --seeds 0 1 2 \\
    --pipelines iterative batch notdd \\
    --samples_per_task 5
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tdd_llm.experiment import ExperimentConfig, ExperimentRunner


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TDD-LLM Experimental Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--task_source", required=True, choices=["known", "unknown"],
        help="Type of task to generate",
    )
    parser.add_argument(
        "--model", default="deepseek-coder:6.7b",
        help="Ollama model name (default: deepseek-coder:6.7b)",
    )
    parser.add_argument(
        "--seeds", nargs="+", type=int, default=[0], metavar="SEED",
        help="Random seeds, one task generated per seed (default: 0)",
    )
    parser.add_argument(
        "--pipelines", nargs="+",
        choices=["iterative", "batch", "notdd"],
        default=["iterative", "batch", "notdd"],
        help="Pipelines to run (default: all three)",
    )
    parser.add_argument(
        "--samples_per_task", type=int, default=5,
        help="Number of independent samples per pipeline per task (default: 5). "
             "Used to compute pass@1 and pass@5.",
    )
    parser.add_argument(
        "--max_iterations", type=int, default=5,
        help="Max iterations for iterative pipeline (default: 5)",
    )
    parser.add_argument(
        "--no_mutation", action="store_true",
        help="Skip mutation testing",
    )
    parser.add_argument(
        "--db", type=Path, default=None,
        help="Path to SQLite database file",
    )
    parser.add_argument("--api_key",  default=None, help="Bearer token for authenticated cloud Ollama endpoints (or set OLLAMA_API_KEY env var)")
    parser.add_argument("--base_url", default=None, help="Ollama base URL (default: http://localhost:11434)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("\n" + "="*60)
    print("  TDD-LLM Experimental Framework")
    print("="*60)
    print(f"  Task source      : {args.task_source}")
    print(f"  Model            : {args.model}")
    print(f"  Seeds            : {args.seeds}")
    print(f"  Pipelines        : {args.pipelines}")
    print(f"  Samples per task : {args.samples_per_task}")
    print(f"  Max iterations   : {args.max_iterations}")
    print(f"  Mutation tests   : {'no' if args.no_mutation else 'yes'}")
    if args.db:
        print(f"  Database         : {args.db}")
    api_key  = args.api_key or os.environ.get("OLLAMA_API_KEY") or None
    base_url = args.base_url or "http://localhost:11434"
    if api_key:
        print(f"  Auth             : Bearer token provided")
    print("="*60 + "\n")

    config = ExperimentConfig(
        task_source=args.task_source,
        model=args.model,
        seeds=args.seeds,
        pipelines=args.pipelines,
        samples_per_task=args.samples_per_task,
        max_iterations=args.max_iterations,
        run_mutation=not args.no_mutation,
        db_path=args.db,
        api_key=api_key,
        base_url=base_url,
    )

    runner = ExperimentRunner(config)

    try:
        runner.run()
    except ConnectionError as e:
        print(f"\n[FATAL] {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[Interrupted] Experiment stopped by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
