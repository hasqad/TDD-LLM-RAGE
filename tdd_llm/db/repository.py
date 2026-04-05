"""
Repository — all database read/write operations.
"""

import sqlite3
from pathlib import Path
from typing import Optional

from .schema import get_connection, DB_PATH


class Repository:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path

    def _conn(self) -> sqlite3.Connection:
        return get_connection(self.db_path)

    # ------------------------------------------------------------------ Tasks

    def insert_task(
        self,
        source: str,
        description: str,
        function_signature: str = "",
        constraints: str = "",
        example_inputs: str = "",
        expected_outputs: str = "",
        seed: Optional[int] = None,
    ) -> int:
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO tasks
                    (source, description, function_signature, constraints,
                     example_inputs, expected_outputs, seed)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (source, description, function_signature, constraints,
                 example_inputs, expected_outputs, seed),
            )
            return cur.lastrowid

    def get_task(self, task_id: int) -> Optional[sqlite3.Row]:
        with self._conn() as conn:
            return conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()

    # ------------------------------------------------------------------- Runs

    def insert_run(
        self,
        task_id: int,
        model: str,
        pipeline: str,
        seed: int,
        samples_per_task: int = 5,
        run_dir: str = "",
    ) -> int:
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO runs
                    (task_id, model, pipeline, seed, samples_per_task, run_dir)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (task_id, model, pipeline, seed, samples_per_task, run_dir),
            )
            return cur.lastrowid

    def update_run_stopped_early(self, run_id: int, error: str = "") -> None:
        with self._conn() as conn:
            conn.execute(
                "UPDATE runs SET stopped_early=1, error_message=? WHERE id=?",
                (error, run_id),
            )

    def get_run(self, run_id: int) -> Optional[sqlite3.Row]:
        with self._conn() as conn:
            return conn.execute(
                "SELECT * FROM runs WHERE id = ?", (run_id,)
            ).fetchone()

    # ------------------------------------------------------- Generated tests

    def insert_generated_tests(
        self, run_id: int, content: str, total_tests: int = 0
    ) -> int:
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO generated_tests (run_id, content, total_tests)
                VALUES (?, ?, ?)
                """,
                (run_id, content, total_tests),
            )
            return cur.lastrowid

    # ---------------------------------------------------------------- Samples

    def insert_sample(
        self,
        run_id: int,
        sample_index: int,
        seed_used: int,
        code: str,
        tests_passed: int,
        tests_total: int,
        passed: bool,
        syntax_error: str = "",
        run_time: float = 0.0,
    ) -> int:
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO samples
                    (run_id, sample_index, seed_used, code,
                     tests_passed, tests_total, passed,
                     syntax_error, run_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (run_id, sample_index, seed_used, code,
                 tests_passed, tests_total, int(passed),
                 syntax_error, run_time),
            )
            return cur.lastrowid

    def get_samples_for_run(self, run_id: int) -> list:
        with self._conn() as conn:
            return conn.execute(
                "SELECT * FROM samples WHERE run_id=? ORDER BY sample_index",
                (run_id,),
            ).fetchall()

    # ----------------------------------------------------- Code iterations

    def insert_code_iteration(
        self,
        sample_id: int,
        iteration: int,
        code: str,
        syntax_error: str = "",
        tests_passed: int = 0,
        tests_total: int = 0,
        feedback: str = "",
    ) -> int:
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO code_iterations
                    (sample_id, iteration, code, syntax_error,
                     tests_passed, tests_total, feedback)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (sample_id, iteration, code, syntax_error,
                 tests_passed, tests_total, feedback),
            )
            return cur.lastrowid

    # ---------------------------------------------------------------- Metrics

    def insert_metrics(self, run_id: int, metrics: dict) -> int:
        with self._conn() as conn:
            cur = conn.execute(
                """
                INSERT OR REPLACE INTO metrics
                    (run_id,
                     pass_at_1, pass_at_5,
                     samples_passed, samples_total,
                     mutation_score, mutants_killed, mutants_total,
                     avg_lines_of_code, avg_cyclomatic_complexity,
                     avg_maintainability_index,
                     avg_run_time_seconds, total_run_time_seconds,
                     total_syntax_errors, avg_attempts)
                VALUES
                    (:run_id,
                     :pass_at_1, :pass_at_5,
                     :samples_passed, :samples_total,
                     :mutation_score, :mutants_killed, :mutants_total,
                     :avg_lines_of_code, :avg_cyclomatic_complexity,
                     :avg_maintainability_index,
                     :avg_run_time_seconds, :total_run_time_seconds,
                     :total_syntax_errors, :avg_attempts)
                """,
                {"run_id": run_id, **metrics},
            )
            return cur.lastrowid

    def get_metrics(self, run_id: int) -> Optional[sqlite3.Row]:
        with self._conn() as conn:
            return conn.execute(
                "SELECT * FROM metrics WHERE run_id=?", (run_id,)
            ).fetchone()

    # -------------------------------------------------------- Summary queries

    def summary_by_pipeline(self) -> list:
        with self._conn() as conn:
            return conn.execute(
                """
                SELECT
                    r.pipeline,
                    COUNT(*)                        AS total_runs,
                    AVG(m.pass_at_1)                AS avg_pass_at_1,
                    AVG(m.pass_at_5)                AS avg_pass_at_5,
                    AVG(m.mutation_score)           AS avg_mutation_score,
                    AVG(m.avg_cyclomatic_complexity) AS avg_complexity,
                    AVG(m.avg_lines_of_code)        AS avg_loc,
                    AVG(m.avg_attempts)             AS avg_attempts,
                    AVG(m.avg_run_time_seconds)     AS avg_runtime
                FROM runs r
                JOIN metrics m ON m.run_id = r.id
                GROUP BY r.pipeline
                ORDER BY r.pipeline
                """
            ).fetchall()

    def summary_by_model_pipeline(self) -> list:
        with self._conn() as conn:
            return conn.execute(
                """
                SELECT
                    r.model,
                    r.pipeline,
                    COUNT(*)                        AS total_runs,
                    AVG(m.pass_at_1)                AS avg_pass_at_1,
                    AVG(m.pass_at_5)                AS avg_pass_at_5,
                    AVG(m.mutation_score)           AS avg_mutation_score,
                    AVG(m.avg_cyclomatic_complexity) AS avg_complexity
                FROM runs r
                JOIN metrics m ON m.run_id = r.id
                GROUP BY r.model, r.pipeline
                ORDER BY r.model, r.pipeline
                """
            ).fetchall()

    def all_runs_detail(self) -> list:
        with self._conn() as conn:
            return conn.execute(
                """
                SELECT
                    r.id            AS run_id,
                    t.source        AS task_source,
                    r.model,
                    r.pipeline,
                    r.seed,
                    r.samples_per_task,
                    m.pass_at_1,
                    m.pass_at_5,
                    m.samples_passed,
                    m.samples_total,
                    m.mutation_score,
                    m.avg_lines_of_code,
                    m.avg_cyclomatic_complexity,
                    m.avg_maintainability_index,
                    m.avg_attempts,
                    m.total_run_time_seconds,
                    r.stopped_early
                FROM runs r
                JOIN tasks t ON t.id = r.task_id
                LEFT JOIN metrics m ON m.run_id = r.id
                ORDER BY r.id
                """
            ).fetchall()
