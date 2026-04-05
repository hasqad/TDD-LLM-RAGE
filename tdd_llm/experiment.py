"""
Experiment orchestrator.

For each (task × model × pipeline × seed) combination, runs N samples
and computes pass@k across them.

Sample seed strategy:
  base_seed = task_seed * 1000 + pipeline_offset
  sample_seed_i = base_seed + i * 100

This ensures samples within a run are varied, but runs are reproducible.
"""

import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .db.schema import init_db, DB_PATH
from .db.repository import Repository
from .evaluation.code_metrics import compute_code_metrics
from .evaluation.mutation_testing import run_mutation_testing
from .evaluation.pass_at_k import compute_pass_at_k
from .evaluation.test_runner import count_tests_in_code
from .pipelines.batch_pipeline import BatchPipeline
from .pipelines.iterative_pipeline import IterativePipeline
from .pipelines.notdd_pipeline import NotddPipeline
from .prompts.task_generator import TaskGenerator
from .utils.file_manager import make_run_dir, save_run_artifacts
from .utils.ollama_client import OllamaClient


@dataclass
class ExperimentConfig:
    task_source: str           # 'known' or 'unknown'
    model: str
    seeds: list[int]
    pipelines: list[str]
    samples_per_task: int = 5
    max_iterations: int = 5
    run_mutation: bool = True
    db_path: Optional[Path] = None
    task_difficulty: str = "medium"  # 'medium' or 'hard', used for unknown task generation
    api_key: Optional[str] = None    # Bearer token for authenticated cloud Ollama endpoints
    base_url: str = "http://localhost:11434"


class ExperimentRunner:
    def __init__(self, config: ExperimentConfig):
        self.config = config
        db_path = config.db_path or DB_PATH
        init_db(db_path)
        self.repo = Repository(db_path)
        self.client = OllamaClient(
            model=config.model,
            base_url=config.base_url,
            api_key=config.api_key,
        )

    def run(self) -> None:
        cfg = self.config
        print(f"\n[Experiment] Checking Ollama connection...")
        if not self.client.is_available():
            raise ConnectionError(
                "Ollama is not running. Start it with: ollama serve"
            )
        print(f"[Experiment] Ollama OK. Model: {cfg.model}")

        task_gen = TaskGenerator(self.client)

        for seed in cfg.seeds:
            print(f"\n{'='*60}")
            print(f"[Experiment] Seed {seed} | source={cfg.task_source}")
            print(f"{'='*60}")

            # Generate task
            print(f"[Experiment] Generating task...")
            try:
                if cfg.task_source == "known":
                    task = task_gen.generate_known(seed=seed)
                else:
                    task = task_gen.generate_unknown(seed=seed, difficulty=cfg.task_difficulty)
            except Exception as e:
                print(f"[ERROR] Task generation failed: {e}")
                continue

            full_desc = task_gen.build_full_description(task)
            print(f"[Experiment] Task: {task.get('title', 'Untitled')}")

            task_id = self.repo.insert_task(
                source=task["source"],
                description=full_desc,
                function_signature=task["function_signature"],
                constraints=task.get("constraints", ""),
                example_inputs=task.get("example_inputs", ""),
                expected_outputs=task.get("expected_outputs", ""),
                seed=seed,
            )

            # Use hardcoded test suite if available (known tasks), otherwise generate with LLM.
            # Hardcoded suites are verified correct, eliminating LLM hallucination issues.
            if task.get("tests_code"):
                if task.get("source") == "unknown":
                    print(f"[Experiment] Using cached validated test suite for '{task.get('title')}'")
                else:
                    print(f"[Experiment] Using hardcoded test suite for '{task.get('title')}'")
                shared_tests_code = task["tests_code"]
            else:
                shared_tests_code = self._generate_validated_tests(task, seed)
                if shared_tests_code is None:
                    print(f"[Experiment] Skipping seed {seed} — no valid test suite could be generated")
                    continue

            for pipeline_name in cfg.pipelines:
                print(f"\n[Pipeline] {pipeline_name.upper()} | seed={seed}")
                self._run_pipeline(task, task_id, pipeline_name, seed, full_desc, shared_tests_code)

        print(f"\n{'='*60}")
        print("[Experiment] Complete!")
        self._print_summary()

    def _generate_validated_tests(self, task: dict, seed: int) -> str:
        """
        Generate a test suite and validate it by running a reference solution against it.
        Retries up to 3 times if the reference solution fails the generated tests.
        This catches LLM-hallucinated wrong expected values before wasting the full run.
        """
        from .evaluation.test_runner import run_tests
        from .pipelines.iterative_pipeline import IterativePipeline
        from .prompts.code_prompts import CODE_GENERATION_PROMPT, CODE_GENERATION_SYSTEM
        from .utils.ollama_client import extract_python_code

        _test_gen = IterativePipeline(self.client, self.config.max_iterations)

        for attempt in range(1, 4):
            test_seed = seed * 1000 + (attempt - 1) * 7
            print(f"[Experiment] Generating shared test suite (seed={test_seed}, attempt {attempt}/3)...")
            try:
                tests_code = _test_gen.generate_tests(task, seed=test_seed)
            except ConnectionError as e:
                print(f"[WARN] Test suite generation timed out — retrying...")
                continue

            try:
                compile(tests_code, "test_suite", "exec")
            except SyntaxError as e:
                print(f"[WARN] Test suite syntax error: {e} — retrying...")
                continue

            # Validate: generate a reference solution and check it passes all tests
            ref_prompt = CODE_GENERATION_PROMPT.format(
                task_description=_test_gen._description(task),
                function_signature=task["function_signature"],
                constraints=task.get("constraints", ""),
                example_inputs=task.get("example_inputs", ""),
                expected_outputs=task.get("expected_outputs", ""),
            )
            try:
                ref_raw = self.client.generate(
                    prompt=ref_prompt, system=CODE_GENERATION_SYSTEM,
                    temperature=0.2, seed=test_seed + 1,
                )
            except ConnectionError as e:
                print(f"[WARN] Reference solution generation timed out — retrying...")
                continue
            ref_code = extract_python_code(ref_raw)
            try:
                result = run_tests(ref_code, tests_code)
            except Exception as e:
                print(f"[WARN] Test runner error: {e} — retrying...")
                continue

            if result.all_passed:
                print(f"[Experiment] Test suite validated ✓ ({result.passed}/{result.total} tests pass on reference solution)")
                # Cache the validated test suite alongside the task
                self._cache_tests(task, tests_code)
                return tests_code
            else:
                print(f"[WARN] Test suite failed validation ({result.passed}/{result.total} tests) — retrying...")

        print(f"[WARN] Could not generate validated test suite after 3 attempts — skipping seed")
        return None

    def _cache_tests(self, task: dict, tests_code: str) -> None:
        from .prompts.task_generator import TASK_CACHE_PATH
        import json
        if not TASK_CACHE_PATH.exists():
            return
        cache = json.loads(TASK_CACHE_PATH.read_text(encoding="utf-8"))
        cache_key = f"{task['seed']}_{self.config.task_difficulty}"
        if cache_key in cache:
            cache[cache_key]["tests_code"] = tests_code
            TASK_CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")
            print(f"[TaskCache] Cached validated test suite for seed={task['seed']}")

    def _run_pipeline(
        self,
        task: dict,
        task_id: int,
        pipeline_name: str,
        seed: int,
        full_desc: str,
        tests_code: str,
    ) -> None:
        cfg = self.config
        run_dir = make_run_dir(task_id, cfg.model, pipeline_name, seed)

        run_id = self.repo.insert_run(
            task_id=task_id,
            model=cfg.model,
            pipeline=pipeline_name,
            seed=seed,
            samples_per_task=cfg.samples_per_task,
            run_dir=str(run_dir),
        )

        try:
            # Build pipeline object
            if pipeline_name == "iterative":
                pipeline = IterativePipeline(self.client, cfg.max_iterations)
            elif pipeline_name == "batch":
                pipeline = BatchPipeline(self.client)
            elif pipeline_name == "notdd":
                pipeline = NotddPipeline(self.client)
            else:
                raise ValueError(f"Unknown pipeline: {pipeline_name}")

            self.repo.insert_generated_tests(
                run_id, tests_code, count_tests_in_code(tests_code)
            )

            # Run N samples
            sample_records = []
            passed_flags = []
            all_code_metrics = []
            total_syntax_errors = 0
            total_attempts = 0

            for i in range(cfg.samples_per_task):
                sample_seed = seed * 1000 + (i + 1) * 100
                print(
                    f"  Sample {i+1}/{cfg.samples_per_task} "
                    f"(seed={sample_seed})...",
                    end=" ", flush=True
                )

                sample = pipeline.run_sample(task, tests_code, seed=sample_seed)

                passed_flags.append(sample.passed)
                total_syntax_errors += sample.syntax_errors
                total_attempts += sample.total_attempts

                status = "PASS" if sample.passed else "FAIL"
                tr = sample.test_result
                tests_passed = tr.passed if tr else 0
                tests_total  = tr.total  if tr else 0
                suffix = f" [syntax: {tr.syntax_error}]" if tr and tr.syntax_error else ""
                print(f"{status} ({tests_passed}/{tests_total} tests){suffix}")

                # Compute code metrics for this sample
                cm = compute_code_metrics(sample.code) if sample.code else None
                if cm:
                    all_code_metrics.append(cm)

                # Store sample in DB
                sample_id = self.repo.insert_sample(
                    run_id=run_id,
                    sample_index=i,
                    seed_used=sample_seed,
                    code=sample.code,
                    tests_passed=tests_passed,
                    tests_total=tests_total,
                    passed=sample.passed,
                    syntax_error=sample.error,
                    run_time=sample.run_time,
                )

                # Store iterations (iterative pipeline only)
                for it in sample.iterations:
                    self.repo.insert_code_iteration(
                        sample_id=sample_id,
                        iteration=it["attempt"],
                        code=it["code"],
                        syntax_error=it.get("syntax_error", ""),
                        tests_passed=it.get("tests_passed", 0),
                        tests_total=it.get("tests_total", 0),
                        feedback=it.get("output", ""),
                    )

                sample_records.append({
                    "index": i,
                    "seed": sample_seed,
                    "code": sample.code,
                    "passed": sample.passed,
                    "tests_passed": tests_passed,
                    "tests_total": tests_total,
                    "syntax_error": sample.error,
                    "run_time": sample.run_time,
                    "iterations": sample.iterations,
                })

            # Compute pass@k
            pak = compute_pass_at_k(passed_flags)
            print(
                f"  pass@1={pak.pass_at_1:.3f}  "
                f"pass@5={pak.pass_at_5:.3f}  "
                f"({pak.c}/{pak.n} samples passed)"
            )

            # Mutation testing on the first passing sample only.
            # Skipped if no sample passed — mutation score is meaningless on failing code.
            mutation_score, mutants_killed, mutants_total = 0.0, 0, 0
            if cfg.run_mutation and tests_code:
                best_code = next(
                    (s["code"] for s in sample_records if s["passed"]), ""
                )
                if best_code:
                    print(f"  Running mutation tests...")
                    mut = run_mutation_testing(best_code, tests_code)
                    if not mut.skipped:
                        mutation_score  = mut.mutation_score
                        mutants_killed  = mut.mutants_killed
                        mutants_total   = mut.mutants_total
                        print(
                            f"  Mutation score: {mutation_score:.2%} "
                            f"({mutants_killed}/{mutants_total})"
                        )
                    else:
                        print(f"  Mutation testing skipped: {mut.error}")

            # Average code metrics across all samples
            n_cm = len(all_code_metrics)
            avg_loc  = sum(m.lines_of_code          for m in all_code_metrics) / n_cm if n_cm else 0
            avg_cc   = sum(m.cyclomatic_complexity   for m in all_code_metrics) / n_cm if n_cm else 0
            avg_mi   = sum(m.maintainability_index   for m in all_code_metrics) / n_cm if n_cm else 0
            avg_time = sum(s["run_time"]             for s in sample_records)   / len(sample_records) if sample_records else 0
            total_time = sum(s["run_time"]           for s in sample_records)

            metrics = {
                "pass_at_1":                round(pak.pass_at_1, 4),
                "pass_at_5":                round(pak.pass_at_5, 4),
                "samples_passed":           pak.c,
                "samples_total":            pak.n,
                "mutation_score":           mutation_score,
                "mutants_killed":           mutants_killed,
                "mutants_total":            mutants_total,
                "avg_lines_of_code":        round(avg_loc,  2),
                "avg_cyclomatic_complexity": round(avg_cc,  2),
                "avg_maintainability_index": round(avg_mi,  2),
                "avg_run_time_seconds":     round(avg_time, 2),
                "total_run_time_seconds":   round(total_time, 2),
                "total_syntax_errors":      total_syntax_errors,
                "avg_attempts":             round(total_attempts / cfg.samples_per_task, 2),
            }
            self.repo.insert_metrics(run_id, metrics)

            save_run_artifacts(
                run_dir=run_dir,
                task_description=full_desc,
                pipeline=pipeline_name,
                tests_code=tests_code,
                samples=sample_records,
                metrics=metrics,
            )

            print(
                f"  Done. pass@1={metrics['pass_at_1']:.3f} | "
                f"mut={metrics['mutation_score']:.2%} | "
                f"LOC={metrics['avg_lines_of_code']:.0f} | "
                f"CC={metrics['avg_cyclomatic_complexity']:.1f}"
            )

        except Exception as e:
            print(f"  [ERROR] {e}")
            self.repo.update_run_stopped_early(run_id, error=str(e)[:500])

    def _print_summary(self) -> None:
        print("\n[Summary by Pipeline]")
        print(
            f"{'Pipeline':<12} {'Runs':>5} {'pass@1':>8} {'pass@5':>8} "
            f"{'MutScore':>10} {'CC':>6} {'LOC':>6} {'Attempts':>9}"
        )
        print("-" * 65)
        for row in self.repo.summary_by_pipeline():
            print(
                f"{row['pipeline']:<12}"
                f"{row['total_runs']:>5}  "
                f"{(row['avg_pass_at_1'] or 0)*100:>7.1f}%"
                f"{(row['avg_pass_at_5'] or 0)*100:>8.1f}%"
                f"{(row['avg_mutation_score'] or 0)*100:>9.1f}%"
                f"{row['avg_complexity'] or 0:>6.1f}"
                f"{row['avg_loc'] or 0:>6.0f}"
                f"{row['avg_attempts'] or 0:>9.1f}"
            )
