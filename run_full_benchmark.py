#!/usr/bin/env python3
"""
TDD-LLM Full Benchmark

Runs the main experiment (pass@k, mutation, LOC, CC) AND HumanEval in one command.
Results are saved to benchmark_results.jsonl so you can compare across runs.

Usage:
    # List available presets
    python3 run_full_benchmark.py --list

    # Run a named preset
    python3 run_full_benchmark.py --preset medium --model llama3.1:8b

    # Run with custom settings (saved under a custom name)
    python3 run_full_benchmark.py --name my_run --seeds 5 17 19 --he_offset 40

    # Show history of past runs
    python3 run_full_benchmark.py --history
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

PRESETS_FILE  = Path(__file__).parent / "benchmark_presets.json"
RESULTS_FILE  = Path(__file__).parent / "benchmark_results.jsonl"


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

def load_presets() -> dict:
    with open(PRESETS_FILE) as f:
        return json.load(f)


def list_presets() -> None:
    presets = load_presets()
    print("\nAvailable presets (benchmark_presets.json):\n")
    for name, cfg in presets.items():
        print(f"  {name:<10}  {cfg['description']}")
        print(f"             seeds={cfg['seeds']}  samples={cfg['samples_per_task']}  "
              f"he_problems={cfg['he_problems']}  he_offset={cfg['he_offset']}  "
              f"mutation={'no' if cfg.get('no_mutation') else 'yes'}")
    print()


# ---------------------------------------------------------------------------
# Results log
# ---------------------------------------------------------------------------

def save_result(entry: dict) -> None:
    with open(RESULTS_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")


def show_history() -> None:
    if not RESULTS_FILE.exists():
        print("No results yet. Run a benchmark first.")
        return

    entries = []
    with open(RESULTS_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))

    if not entries:
        print("No results yet.")
        return

    print(f"\n{'='*80}")
    print("  Benchmark History")
    print(f"{'='*80}")
    print(f"{'Run':<22} {'Preset':<10} {'Model':<16} "
          f"{'Pipeline':<12} {'pass@1':>7} {'MutScore':>9} {'HumanEval':>10}")
    print("-" * 80)

    for e in entries:
        ts  = e.get("timestamp", "")[:19].replace("T", " ")
        pre = e.get("preset", "custom")
        mdl = e.get("model", "")[:15]
        for name, m in e.get("pipelines", {}).items():
            p1   = m.get("pass_at_1",       0) * 100
            mut  = m.get("mutation_score",  0) * 100
            he   = m.get("humaneval_pass1", 0) * 100
            print(f"{ts:<22} {pre:<10} {mdl:<16} {name:<12} "
                  f"{p1:>6.1f}% {mut:>8.1f}% {he:>9.1f}%")
        print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="TDD-LLM Full Benchmark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Meta actions
    p.add_argument("--list",    action="store_true", help="List available presets and exit")
    p.add_argument("--history", action="store_true", help="Show history of past runs and exit")

    # Run identity
    p.add_argument("--preset", default=None, help="Named preset from benchmark_presets.json")
    p.add_argument("--name",   default=None, help="Custom name for this run (saved in history)")
    p.add_argument("--model",  default="llama3.1:8b")
    p.add_argument("--models", nargs="+", default=None, help="Run multiple models sequentially")
    p.add_argument("--api_key",  default=None, help="Bearer token for authenticated cloud Ollama endpoints (or set OLLAMA_API_KEY env var)")
    p.add_argument("--base_url", default=None, help="Ollama base URL (default: http://localhost:11434)")

    # Override any preset value
    p.add_argument("--seeds",           nargs="+", type=int, default=None)
    p.add_argument("--samples_per_task", type=int, default=None)
    p.add_argument("--max_iterations",   type=int, default=None)
    p.add_argument("--he_problems",      type=int, default=None)
    p.add_argument("--he_offset",        type=int, default=None)
    p.add_argument("--no_mutation",      action="store_true", default=None)
    p.add_argument("--no_humaneval",     action="store_true", help="Skip HumanEval benchmark")
    p.add_argument(
        "--pipelines", nargs="+",
        choices=["iterative", "batch", "notdd"],
        default=["iterative", "batch", "notdd"],
    )
    return p.parse_args()


def resolve_config(args) -> dict:
    """Merge preset defaults with CLI overrides."""
    defaults = {
        "seeds": [5, 17, 19],
        "samples_per_task": 5,
        "max_iterations": 5,
        "he_problems": 20,
        "he_offset": 30,
        "no_mutation": False,
    }

    if args.preset:
        presets = load_presets()
        if args.preset not in presets:
            print(f"[ERROR] Unknown preset '{args.preset}'. Run --list to see options.")
            sys.exit(1)
        defaults.update(presets[args.preset])

    # CLI overrides win
    if args.seeds           is not None: defaults["seeds"]           = args.seeds
    if args.samples_per_task is not None: defaults["samples_per_task"] = args.samples_per_task
    if args.max_iterations  is not None: defaults["max_iterations"]  = args.max_iterations
    if args.he_problems     is not None: defaults["he_problems"]     = args.he_problems
    if args.he_offset       is not None: defaults["he_offset"]       = args.he_offset
    if args.no_mutation:                 defaults["no_mutation"]     = True

    return defaults


# ---------------------------------------------------------------------------
# Benchmark runners
# ---------------------------------------------------------------------------

def run_main_experiment(cfg: dict, model: str, pipelines: list, api_key: str = None, base_url: str = None) -> dict:
    import tempfile
    import uuid
    from pathlib import Path as _Path
    from tdd_llm.experiment import ExperimentConfig, ExperimentRunner
    from tdd_llm.utils.ollama_client import OLLAMA_BASE_URL

    print("\n" + "=" * 60)
    print("  PART 1 — Main Experiment")
    print("  (pass@k, mutation score, LOC, cyclomatic complexity)")
    print("=" * 60)

    # Use a fresh temporary database so old historical runs don't contaminate
    # this run's summary. Results are persisted via benchmark_results.jsonl.
    tmp_db = _Path(tempfile.gettempdir()) / f"tdd_llm_{uuid.uuid4().hex}.db"

    config = ExperimentConfig(
        task_source=cfg.get("task_source", "known"),
        task_difficulty=cfg.get("task_difficulty", "medium"),
        model=model,
        seeds=cfg["seeds"],
        pipelines=pipelines,
        samples_per_task=cfg["samples_per_task"],
        max_iterations=cfg["max_iterations"],
        run_mutation=not cfg["no_mutation"],
        db_path=tmp_db,
        api_key=api_key,
        base_url=base_url or OLLAMA_BASE_URL,
    )
    runner = ExperimentRunner(config)
    try:
        runner.run()
        return {r["pipeline"]: dict(r) for r in runner.repo.summary_by_pipeline()}
    finally:
        tmp_db.unlink(missing_ok=True)


def run_humaneval(cfg: dict, model: str, pipelines: list, api_key: str = None, base_url: str = None) -> dict:
    from tdd_llm.evaluation.humaneval import load_problems, evaluate_pipeline
    from tdd_llm.pipelines.batch_pipeline import BatchPipeline
    from tdd_llm.pipelines.iterative_pipeline import IterativePipeline
    from tdd_llm.pipelines.notdd_pipeline import NotddPipeline
    from tdd_llm.utils.ollama_client import OllamaClient, OLLAMA_BASE_URL

    print("\n" + "=" * 60)
    print("  PART 2 — HumanEval Benchmark")
    print(f"  (problems {cfg['he_offset']}–{cfg['he_offset'] + cfg['he_problems'] - 1})")
    print("=" * 60)

    problems = load_problems(n=cfg["he_problems"], offset=cfg["he_offset"])
    print(f"\n[HumanEval] Loaded {len(problems)} problems\n")

    seed_offsets = {"iterative": 0, "batch": 0, "notdd": 0}
    results = {}

    for name in pipelines:
        print(f"{'='*60}")
        print(f"Pipeline: {name.upper()}")
        print(f"{'='*60}")

        client = OllamaClient(model=model, base_url=base_url or OLLAMA_BASE_URL, api_key=api_key)

        if name == "iterative":
            pipeline = IterativePipeline(client, max_iterations=cfg["max_iterations"])
        elif name == "batch":
            pipeline = BatchPipeline(client)
        else:
            pipeline = NotddPipeline(client)

        result = evaluate_pipeline(
            pipeline_name=name,
            pipeline=pipeline,
            problems=problems,
            samples_per_problem=1,
            seed_offset=seed_offsets[name],
        )
        results[name] = result
        print(f"\n  {name}: {result.problems_passed}/{result.problems_total} "
              f"passed  pass@1={result.pass_at_1:.3f}\n")

    return results


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

def print_unified_summary(main_metrics: dict, he_results: dict, pipelines: list) -> None:
    print("\n" + "=" * 70)
    print("  FULL BENCHMARK SUMMARY")
    print("=" * 70)
    print(f"{'Pipeline':<12} {'pass@1':>7} {'pass@5':>7} {'MutScore':>9} "
          f"{'LOC':>5} {'CC':>5} {'Attempts':>9} {'HumanEval':>10}")
    print("-" * 70)
    for name in pipelines:
        m   = main_metrics.get(name, {})
        he  = he_results.get(name)
        p1  = (m.get("avg_pass_at_1")      or 0) * 100
        p5  = (m.get("avg_pass_at_5")      or 0) * 100
        mut = (m.get("avg_mutation_score") or 0) * 100
        loc = m.get("avg_loc")             or 0
        cc  = m.get("avg_complexity")      or 0
        att = m.get("avg_attempts")        or 0
        he_p1 = (he.pass_at_1 * 100) if he else 0.0
        print(f"{name:<12} {p1:>6.1f}% {p5:>6.1f}% {mut:>8.1f}% "
              f"{loc:>5.0f} {cc:>5.1f} {att:>9.1f} {he_p1:>9.1f}%")
    print()


def build_result_entry(
    run_name: str, preset: str, model: str, cfg: dict,
    pipelines: list, main_metrics: dict, he_results: dict,
) -> dict:
    entry = {
        "timestamp": datetime.now().isoformat(),
        "name":   run_name,
        "preset": preset,
        "model":  model,
        "config": cfg,
        "pipelines": {},
    }
    for name in pipelines:
        m  = main_metrics.get(name, {})
        he = he_results.get(name)
        entry["pipelines"][name] = {
            "pass_at_1":       round((m.get("avg_pass_at_1")      or 0), 4),
            "pass_at_5":       round((m.get("avg_pass_at_5")      or 0), 4),
            "mutation_score":  round((m.get("avg_mutation_score") or 0), 4),
            "avg_loc":         round((m.get("avg_loc")            or 0), 1),
            "avg_cc":          round((m.get("avg_complexity")     or 0), 2),
            "avg_attempts":    round((m.get("avg_attempts")       or 0), 2),
            "humaneval_pass1": round(he.pass_at_1, 4) if he else 0.0,
        }
    return entry


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------



def print_cross_model_summary(all_results: list[dict], pipelines: list) -> None:
    """Print a final comparison table across all models."""
    print("\n" + "=" * 80)
    print("  CROSS-MODEL SUMMARY")
    print("=" * 80)
    print(f"{'Model':<24} {'Pipeline':<12} {'pass@1':>7} {'MutScore':>9} {'HumanEval':>10}")
    print("-" * 64)
    for model, main_metrics, he_results in all_results:
        for name in pipelines:
            m   = main_metrics.get(name, {})
            he  = he_results.get(name)
            p1  = (m.get("avg_pass_at_1")      or 0) * 100
            mut = (m.get("avg_mutation_score") or 0) * 100
            he_p1 = (he.pass_at_1 * 100) if he else 0.0
            print(f"{model:<24} {name:<12} {p1:>6.1f}% {mut:>8.1f}% {he_p1:>9.1f}%")
        print()


def main() -> None:
    args = parse_args()

    if args.list:
        list_presets()
        return

    if args.history:
        show_history()
        return

    cfg = resolve_config(args)

    # Resolve API key: CLI flag > env var
    api_key  = args.api_key or os.environ.get("OLLAMA_API_KEY") or None
    base_url = args.base_url or None

    # Build list of models to run
    models = args.models if args.models else [args.model]

    try:
        all_results = []
        for model in models:
            if len(models) > 1:
                print(f"\n{'#'*60}")
                print(f"  Running model {models.index(model)+1}/{len(models)}: {model}")
                print(f"{'#'*60}")
            main_metrics = None
            he_results   = None

            run_name = args.name or args.preset or "custom"
            preset   = args.preset or "custom"

            print("\n" + "=" * 60)
            print("  TDD-LLM Full Benchmark")
            print("=" * 60)
            print(f"  Run name         : {run_name}")
            print(f"  Model            : {model}")
            print(f"  Seeds            : {cfg['seeds']}")
            print(f"  Samples/task     : {cfg['samples_per_task']}")
            print(f"  Max iterations   : {cfg['max_iterations']}")
            print(f"  HumanEval        : {cfg['he_problems']} problems (offset {cfg['he_offset']})")
            print(f"  Mutation tests   : {'no' if cfg['no_mutation'] else 'yes'}")
            print(f"  Pipelines        : {args.pipelines}")
            if api_key:
                print(f"  Auth             : Bearer token provided")
            if base_url:
                print(f"  Base URL         : {base_url}")
            print("=" * 60)

            from tdd_llm.utils.ollama_client import OllamaClient, OLLAMA_BASE_URL
            client = OllamaClient(model=model, base_url=base_url or OLLAMA_BASE_URL, api_key=api_key)
            if not client.is_available():
                print(f"\n[SKIP] Ollama model '{model}' not available. Skipping.")
                continue

            main_metrics = run_main_experiment(cfg, model, args.pipelines, api_key=api_key, base_url=base_url)
            he_results   = {} if args.no_humaneval else run_humaneval(cfg, model, args.pipelines, api_key=api_key, base_url=base_url)
            print_unified_summary(main_metrics, he_results, args.pipelines)

            entry = build_result_entry(
                run_name, preset, model, cfg,
                args.pipelines, main_metrics, he_results,
            )
            save_result(entry)
            print(f"[Results] Saved to {RESULTS_FILE}")
            all_results.append((model, main_metrics, he_results))

        if len(models) > 1 and all_results:
            print_cross_model_summary(all_results, args.pipelines)

    except KeyboardInterrupt:
        print("\n[Interrupted]")
        sys.exit(0)


if __name__ == "__main__":
    main()
