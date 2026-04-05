#!/usr/bin/env python3
"""
HumanEval Benchmark — CLI

Evaluates each pipeline on OpenAI's HumanEval dataset (ground-truth tests).
Produces pass@1 scores between 0 and 1 for each pipeline.

Usage:
    python3 run_humaneval.py --model llama3.1:8b --n_problems 20
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tdd_llm.evaluation.humaneval import load_problems, evaluate_pipeline
from tdd_llm.pipelines.batch_pipeline import BatchPipeline
from tdd_llm.pipelines.iterative_pipeline import IterativePipeline
from tdd_llm.pipelines.notdd_pipeline import NotddPipeline
from tdd_llm.utils.ollama_client import OllamaClient


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HumanEval Benchmark")
    parser.add_argument("--model", default="llama3.1:8b")
    parser.add_argument(
        "--n_problems", type=int, default=164,
        help="Number of HumanEval problems to evaluate (max 164, default 164)",
    )
    parser.add_argument(
        "--offset", type=int, default=0,
        help="Skip the first N problems (default 0)",
    )
    parser.add_argument(
        "--pipelines", nargs="+",
        choices=["iterative", "batch", "notdd"],
        default=["iterative", "batch", "notdd"],
    )
    parser.add_argument(
        "--max_iterations", type=int, default=5,
        help="Max iterations for iterative pipeline",
    )
    parser.add_argument("--api_key",  default=None, help="Bearer token for authenticated cloud Ollama endpoints (or set OLLAMA_API_KEY env var)")
    parser.add_argument("--base_url", default=None, help="Ollama base URL (default: http://localhost:11434)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("\n" + "=" * 60)
    print("  HumanEval Benchmark")
    print("=" * 60)
    print(f"  Model      : {args.model}")
    print(f"  Problems   : {args.n_problems} (offset {args.offset})")
    print(f"  Pipelines  : {args.pipelines}")
    print("=" * 60 + "\n")

    api_key  = args.api_key or os.environ.get("OLLAMA_API_KEY") or None
    base_url = args.base_url or "http://localhost:11434"

    client = OllamaClient(model=args.model, base_url=base_url, api_key=api_key)
    if not client.is_available():
        print("[FATAL] Ollama is not running. Start with: ollama serve")
        sys.exit(1)
    print(f"[HumanEval] Ollama OK. Model: {args.model}\n")

    problems = load_problems(n=args.n_problems, offset=args.offset)
    print(f"[HumanEval] Loaded {len(problems)} problems\n")

    results = []
    for name in args.pipelines:
        print(f"{'='*60}")
        print(f"Pipeline: {name.upper()}")
        print(f"{'='*60}")

        if name == "iterative":
            pipeline = IterativePipeline(client, max_iterations=args.max_iterations)
        elif name == "batch":
            pipeline = BatchPipeline(client)
        else:
            pipeline = NotddPipeline(client)

        seed_offsets = {"iterative": 0, "batch": 500, "notdd": 999}
        result = evaluate_pipeline(
            pipeline_name=name,
            pipeline=pipeline,
            problems=problems,
            samples_per_problem=1,
            seed_offset=seed_offsets[name],
        )
        results.append(result)
        print(
            f"\n  {name}: {result.problems_passed}/{result.problems_total} "
            f"passed  pass@1={result.pass_at_1:.3f}\n"
        )

    # Summary
    print("\n" + "=" * 60)
    print("  HumanEval Summary")
    print("=" * 60)
    print(f"{'Pipeline':<12} {'pass@1':>8} {'Passed':>8} {'Total':>8}")
    print("-" * 40)
    for r in results:
        print(
            f"{r.pipeline:<12} {r.pass_at_1:>8.3f} "
            f"{r.problems_passed:>8} {r.problems_total:>8}"
        )
    print()


if __name__ == "__main__":
    main()
