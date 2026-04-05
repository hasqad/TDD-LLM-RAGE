# TDD-LLM Experimental Framework

Compares three LLM development strategies using **pass@k** as the primary metric:

| Pipeline     | Description                                    |
|--------------|------------------------------------------------|
| iterative    | Generate tests → loop on code until pass       |
| batch        | Generate tests + code once, no feedback        |
| notdd        | Generate code directly, evaluate independently |

---

## Architecture

```
tdd_llm/
│
├── run_experiment.py              ← entry point
├── analyze_results.py             ← results & reporting
├── requirements.txt
│
├── data/
│   └── experiments.db             ← SQLite (auto-created)
│
├── runs/                          ← artifact storage (auto-created)
│   └── run_<ts>_task1_iterative_seed0/
│       ├── query.txt
│       ├── iterative_tests.py
│       ├── metrics.json
│       └── samples/
│           ├── sample_000/
│           │   ├── solution.py
│           │   ├── result.json
│           │   └── iterations/    ← iterative pipeline only
│           │       ├── iteration_001.json
│           │       └── iteration_002.json
│           ├── sample_001/
│           └── ...
│
└── tdd_llm/
    ├── __init__.py
    ├── experiment.py              ← orchestrator
    │
    ├── db/
    │   ├── schema.py              ← SQLite schema (5 tables)
    │   └── repository.py          ← all CRUD + aggregate queries
    │
    ├── evaluation/
    │   ├── pass_at_k.py           ← unbiased pass@k formula
    │   ├── test_runner.py         ← subprocess + pytest
    │   ├── mutation_testing.py    ← cosmic-ray integration
    │   └── code_metrics.py        ← LOC, CC, MI (radon or AST)
    │
    ├── pipelines/
    │   ├── iterative_pipeline.py
    │   ├── batch_pipeline.py
    │   └── notdd_pipeline.py
    │
    ├── prompts/
    │   ├── task_prompts.py        ← known/unknown task templates
    │   ├── code_prompts.py        ← test + code generation templates
    │   └── task_generator.py
    │
    └── utils/
        ├── ollama_client.py       ← Ollama HTTP API
        └── file_manager.py        ← artifact saving
```

---

## Database Tables

```
tasks            — generated problems
runs             — one per (task × model × pipeline × seed)
generated_tests  — shared test suite per run
samples          — one row per individual solution attempt
code_iterations  — intermediate steps within iterative samples
metrics          — aggregated pass@k + all quality scores per run
```

---

## Setup

```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull deepseek-coder:6.7b

# 2. Start Ollama
ollama serve

# 3. Install Python deps
pip install -r requirements.txt
```

---

## Running Experiments

```bash
# Standard run — 3 seeds, 5 samples per task, all pipelines
python run_experiment.py \
  --task_source known \
  --model deepseek-coder:6.7b \
  --seeds 0 1 2 \
  --pipelines iterative batch notdd \
  --samples_per_task 5

# Quick test — skip mutation, 1 seed, 2 samples
python run_experiment.py \
  --task_source known \
  --model codellama \
  --seeds 0 \
  --samples_per_task 2 \
  --no_mutation

# Unknown tasks with higher sample count
python run_experiment.py \
  --task_source unknown \
  --model qwen2.5-coder \
  --seeds 0 1 2 3 4 \
  --samples_per_task 10
```

### All CLI options

| Flag                | Default                   | Description                              |
|---------------------|---------------------------|------------------------------------------|
| `--task_source`     | required                  | `known` or `unknown`                     |
| `--model`           | `deepseek-coder:6.7b`     | Ollama model name                        |
| `--seeds`           | `[0]`                     | One task generated per seed              |
| `--pipelines`       | all three                 | `iterative batch notdd`                  |
| `--samples_per_task`| `5`                       | Samples per pipeline per task            |
| `--max_iterations`  | `5`                       | Max iterations in iterative pipeline     |
| `--no_mutation`     | off                       | Skip cosmic-ray                          |
| `--db`              | `data/experiments.db`     | Custom database path                     |

---

## Analyzing Results

```bash
python analyze_results.py
python analyze_results.py --export results.csv
```

---

## pass@k Explained

For each run (task × pipeline), N independent samples are generated.
Each sample gets a different seed, so the LLM produces varied solutions.

```
pass@k = 1 - C(n-c, k) / C(n, k)

n = samples generated (your --samples_per_task)
c = samples that passed all tests
k = 1 or 5
```

**pass@1** — probability a single random sample passes.
**pass@5** — probability at least one of 5 random samples passes.

With 5 samples this is computed exactly. With 10 samples you also get
a statistically tighter estimate of pass@5.

---

## Expected Results

| Pipeline     | pass@1 | pass@5 | Mutation | CC     |
|--------------|--------|--------|----------|--------|
| iterative    | high   | high   | high     | low    |
| batch        | medium | medium | medium   | medium |
| notdd        | low    | medium | low      | high   |

The iterative feedback loop forces the model to satisfy explicit test
cases, producing more correct and more testable code than the other two.
