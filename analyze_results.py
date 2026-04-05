#!/usr/bin/env python3
"""
TDD-LLM Results Analysis

Reads from benchmark_results.jsonl (written by run_full_benchmark.py).

python analyze_results.py
python analyze_results.py --export results.csv
python analyze_results.py --preset very_hard
python analyze_results.py --model qwen2.5-coder:7b
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

RESULTS_FILE = Path(__file__).parent / "benchmark_results.jsonl"
PIPELINES = ["iterative", "batch", "notdd"]


def parse_args():
    parser = argparse.ArgumentParser(description="Analyze TDD-LLM results")
    parser.add_argument("--results", type=Path, default=RESULTS_FILE)
    parser.add_argument("--export", type=Path, default=None, help="Export all runs to CSV")
    parser.add_argument("--preset", default=None, help="Filter by preset name")
    parser.add_argument("--model",  default=None, help="Filter by model name (partial match)")
    return parser.parse_args()


def load_entries(path: Path, preset_filter=None, model_filter=None) -> list[dict]:
    if not path.exists():
        print(f"Results file not found: {path}")
        print("Run a benchmark first: python run_full_benchmark.py ...")
        sys.exit(1)

    entries = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            e = json.loads(line)
            if preset_filter and e.get("preset") != preset_filter:
                continue
            if model_filter and model_filter not in e.get("model", ""):
                continue
            entries.append(e)
    return entries


def divider(width=78):
    print("=" * width)


# ---------------------------------------------------------------------------
# Summary by pipeline (averaged across all matching runs)
# ---------------------------------------------------------------------------

def summary_by_pipeline(entries: list[dict]) -> None:
    totals = defaultdict(lambda: defaultdict(float))
    counts = defaultdict(int)

    for e in entries:
        for name, m in e.get("pipelines", {}).items():
            counts[name] += 1
            for key in ("pass_at_1", "pass_at_5", "mutation_score",
                        "avg_loc", "avg_cc", "avg_attempts", "humaneval_pass1"):
                totals[name][key] += m.get(key) or 0

    if not counts:
        print("No data.")
        return

    divider()
    print("  Summary by Pipeline (averaged across all runs)")
    divider()
    print(f"{'Pipeline':<12} {'Runs':>5} {'pass@1':>8} {'pass@5':>8} "
          f"{'MutScore':>10} {'LOC':>6} {'CC':>6} {'Attempts':>9} {'HumanEval':>10}")
    print("-" * 78)

    for name in PIPELINES:
        if name not in counts:
            continue
        n = counts[name]
        t = totals[name]
        print(
            f"{name:<12} {n:>5}"
            f"  {t['pass_at_1']/n*100:>6.1f}%"
            f"  {t['pass_at_5']/n*100:>6.1f}%"
            f"  {t['mutation_score']/n*100:>8.1f}%"
            f"  {t['avg_loc']/n:>5.1f}"
            f"  {t['avg_cc']/n:>5.1f}"
            f"  {t['avg_attempts']/n:>8.1f}"
            f"  {t['humaneval_pass1']/n*100:>8.1f}%"
        )


# ---------------------------------------------------------------------------
# Summary by model x pipeline
# ---------------------------------------------------------------------------

def summary_by_model_pipeline(entries: list[dict]) -> None:
    totals = defaultdict(lambda: defaultdict(float))
    counts = defaultdict(int)

    for e in entries:
        model = e.get("model", "unknown")
        for name, m in e.get("pipelines", {}).items():
            key = (model, name)
            counts[key] += 1
            for k in ("pass_at_1", "pass_at_5", "mutation_score", "humaneval_pass1"):
                totals[key][k] += m.get(k) or 0

    if not counts:
        return

    divider()
    print("  Summary by Model x Pipeline")
    divider()
    print(f"{'Model':<22} {'Pipeline':<12} {'Runs':>5} {'pass@1':>8} "
          f"{'pass@5':>8} {'MutScore':>10} {'HumanEval':>10}")
    print("-" * 78)

    for (model, name), n in sorted(counts.items()):
        t = totals[(model, name)]
        print(
            f"{model:<22} {name:<12} {n:>5}"
            f"  {t['pass_at_1']/n*100:>6.1f}%"
            f"  {t['pass_at_5']/n*100:>6.1f}%"
            f"  {t['mutation_score']/n*100:>8.1f}%"
            f"  {t['humaneval_pass1']/n*100:>8.1f}%"
        )


# ---------------------------------------------------------------------------
# All runs detail
# ---------------------------------------------------------------------------

def all_runs_detail(entries: list[dict]) -> list[dict]:
    rows = []
    for e in entries:
        ts          = e.get("timestamp", "")[:19].replace("T", " ")
        preset      = e.get("preset", "custom")
        model       = e.get("model", "")
        task_source = e.get("config", {}).get("task_source", "known")
        for name in PIPELINES:
            m = e.get("pipelines", {}).get(name)
            if not m:
                continue
            rows.append({
                "timestamp":       ts,
                "preset":          preset,
                "model":           model,
                "task_source":     task_source,
                "pipeline":        name,
                "pass_at_1":       m.get("pass_at_1", 0),
                "pass_at_5":       m.get("pass_at_5", 0),
                "mutation_score":  m.get("mutation_score", 0),
                "humaneval_pass1": m.get("humaneval_pass1", 0),
                "avg_loc":         m.get("avg_loc", 0),
                "avg_cc":          m.get("avg_cc", 0),
                "avg_attempts":    m.get("avg_attempts", 0),
            })
    return rows


def print_all_runs(rows: list[dict]) -> None:
    divider()
    print("  All Runs Detail")
    divider()
    print(f"{'Timestamp':<20} {'Preset':<12} {'Model':<22} {'Source':<8} "
          f"{'Pipeline':<12} {'pass@1':>8} {'MutScore':>10} {'HumanEval':>10}")
    print("-" * 110)
    for r in rows:
        print(
            f"{r['timestamp']:<20} {r['preset']:<12} {r['model']:<22} "
            f"{r['task_source']:<8} {r['pipeline']:<12}"
            f"  {r['pass_at_1']*100:>6.1f}%"
            f"  {r['mutation_score']*100:>8.1f}%"
            f"  {r['humaneval_pass1']*100:>8.1f}%"
        )


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

def interpretation(entries: list[dict]) -> None:
    totals = defaultdict(lambda: defaultdict(float))
    counts = defaultdict(int)

    for e in entries:
        for name, m in e.get("pipelines", {}).items():
            counts[name] += 1
            for k in ("pass_at_1", "pass_at_5", "mutation_score", "humaneval_pass1"):
                totals[name][k] += m.get(k) or 0

    if not counts:
        return

    avgs = {
        name: {k: totals[name][k] / counts[name] for k in totals[name]}
        for name in counts
    }

    divider()
    print("  Interpretation")
    divider()

    metrics = [
        ("pass@1",         "pass_at_1",       True),
        ("pass@5",         "pass_at_5",       True),
        ("mutation score", "mutation_score",   True),
        ("HumanEval",      "humaneval_pass1",  True),
    ]

    for label, key, higher_better in metrics:
        vals = {p: avgs[p][key] for p in avgs if key in avgs[p]}
        if not vals:
            continue
        best = max(vals, key=vals.get) if higher_better else min(vals, key=vals.get)
        print(f"\n  {label.upper()}")
        for p in PIPELINES:
            if p not in vals:
                continue
            marker = " <- best" if p == best else ""
            print(f"    {p:<12} {vals[p]*100:.1f}%{marker}")

    it = avgs.get("iterative", {})
    nt = avgs.get("notdd", {})
    bt = avgs.get("batch", {})

    if it and nt:
        print(f"\n  Iterative vs No-TDD:  pass@1 delta         = {(it['pass_at_1'] - nt['pass_at_1'])*100:+.1f}%")
        print(f"  Iterative vs No-TDD:  mutation score delta  = {(it['mutation_score'] - nt['mutation_score'])*100:+.1f}%")
        print(f"  Iterative vs No-TDD:  HumanEval delta       = {(it['humaneval_pass1'] - nt['humaneval_pass1'])*100:+.1f}%")
    if it and bt:
        print(f"  Iterative vs Batch:   pass@1 delta          = {(it['pass_at_1'] - bt['pass_at_1'])*100:+.1f}%")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    entries = load_entries(args.results, args.preset, args.model)

    if not entries:
        print("No matching results found.")
        sys.exit(0)

    print(f"\n[Loaded {len(entries)} benchmark runs from {args.results}]")
    if args.preset:
        print(f"[Filter: preset={args.preset}]")
    if args.model:
        print(f"[Filter: model contains '{args.model}']")

    summary_by_pipeline(entries)
    summary_by_model_pipeline(entries)

    rows = all_runs_detail(entries)
    print_all_runs(rows)

    interpretation(entries)

    if args.export and rows:
        with open(args.export, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        print(f"\n[Export] {len(rows)} rows saved to {args.export}")


if __name__ == "__main__":
    main()
