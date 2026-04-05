"""
SQLite database schema for TDD-LLM experiments.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "experiments.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

-- Generated programming tasks
CREATE TABLE IF NOT EXISTS tasks (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    source              TEXT NOT NULL CHECK(source IN ('known', 'unknown')),
    description         TEXT NOT NULL,
    function_signature  TEXT,
    constraints         TEXT,
    example_inputs      TEXT,
    expected_outputs    TEXT,
    seed                INTEGER
);

-- One run = one (task x model x pipeline x seed) experiment
CREATE TABLE IF NOT EXISTS runs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    task_id         INTEGER NOT NULL REFERENCES tasks(id),
    model           TEXT NOT NULL,
    pipeline        TEXT NOT NULL CHECK(pipeline IN ('iterative', 'batch', 'notdd')),
    seed            INTEGER NOT NULL,
    samples_per_task INTEGER DEFAULT 5,
    run_dir         TEXT,
    stopped_early   INTEGER DEFAULT 0,
    error_message   TEXT
);

-- Generated test code per run
CREATE TABLE IF NOT EXISTS generated_tests (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id      INTEGER NOT NULL REFERENCES runs(id),
    content     TEXT,
    total_tests INTEGER DEFAULT 0
);

-- Each individual sample (one solution attempt)
-- A run has samples_per_task of these
CREATE TABLE IF NOT EXISTS samples (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          INTEGER NOT NULL REFERENCES runs(id),
    sample_index    INTEGER NOT NULL,   -- 0-based index within the run
    seed_used       INTEGER,
    code            TEXT,
    tests_passed    INTEGER DEFAULT 0,
    tests_total     INTEGER DEFAULT 0,
    passed          INTEGER DEFAULT 0,  -- boolean: did ALL tests pass?
    syntax_error    TEXT,
    run_time        REAL DEFAULT 0.0
);

-- Iterative-only: intermediate code iterations within a single sample
CREATE TABLE IF NOT EXISTS code_iterations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id       INTEGER NOT NULL REFERENCES samples(id),
    iteration       INTEGER NOT NULL DEFAULT 1,
    code            TEXT,
    syntax_error    TEXT,
    tests_passed    INTEGER DEFAULT 0,
    tests_total     INTEGER DEFAULT 0,
    feedback        TEXT
);

-- Final aggregated metrics per run (across all samples)
CREATE TABLE IF NOT EXISTS metrics (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id                  INTEGER NOT NULL UNIQUE REFERENCES runs(id),

    -- pass@k  (computed across all samples in the run)
    pass_at_1               REAL DEFAULT 0.0,
    pass_at_5               REAL DEFAULT 0.0,
    samples_passed          INTEGER DEFAULT 0,   -- how many samples passed
    samples_total           INTEGER DEFAULT 0,

    -- mutation testing (averaged across passing samples)
    mutation_score          REAL DEFAULT 0.0,
    mutants_killed          INTEGER DEFAULT 0,
    mutants_total           INTEGER DEFAULT 0,

    -- code quality (averaged across all samples)
    avg_lines_of_code       REAL DEFAULT 0.0,
    avg_cyclomatic_complexity REAL DEFAULT 0.0,
    avg_maintainability_index REAL DEFAULT 0.0,

    -- runtime
    avg_run_time_seconds    REAL DEFAULT 0.0,
    total_run_time_seconds  REAL DEFAULT 0.0,

    -- error counts
    total_syntax_errors     INTEGER DEFAULT 0,
    avg_attempts            REAL DEFAULT 0.0
);
"""


def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path = DB_PATH) -> None:
    """Create all tables if they don't exist."""
    conn = get_connection(db_path)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"[DB] Initialized at {db_path}")
