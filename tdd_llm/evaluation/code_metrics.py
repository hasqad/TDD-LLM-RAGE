"""
Code quality metrics: LOC, cyclomatic complexity, maintainability index.
Tries radon first, falls back to AST-based computation.
"""

import ast
import math
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CodeMetrics:
    lines_of_code: int = 0
    cyclomatic_complexity: float = 0.0
    maintainability_index: float = 0.0


def count_lines_of_code(code: str) -> int:
    return sum(
        1 for line in code.splitlines()
        if line.strip() and not line.strip().startswith("#")
    )


def _cc_from_ast(code: str) -> float:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return 0.0
    branch_nodes = (
        ast.If, ast.For, ast.While, ast.ExceptHandler,
        ast.With, ast.Assert,
        ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp,
        ast.BoolOp,
    )
    count = 1
    for node in ast.walk(tree):
        if isinstance(node, branch_nodes):
            count += 1
    return float(count)


def _mi_from_values(code: str, cc: float, loc: int) -> float:
    tokens = re.findall(r"\w+|[^\w\s]", code)
    hv = len(tokens) + 1
    try:
        mi = 171 - 5.2 * math.log(hv) - 0.23 * cc - 16.2 * math.log(loc + 1)
        return round(max(0.0, min(100.0, mi)), 2)
    except (ValueError, ZeroDivisionError):
        return 0.0


def _try_radon(code: str) -> tuple[float, float] | None:
    check = subprocess.run(
        [sys.executable, "-c", "import radon"],
        capture_output=True
    )
    if check.returncode != 0:
        return None

    with tempfile.NamedTemporaryFile(
        suffix=".py", mode="w", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        fname = f.name

    try:
        cc_proc = subprocess.run(
            [sys.executable, "-m", "radon", "cc", "-s", "-a", fname],
            capture_output=True, text=True
        )
        mi_proc = subprocess.run(
            [sys.executable, "-m", "radon", "mi", "-s", fname],
            capture_output=True, text=True
        )
        cc_avg = re.search(r"Average complexity.*?([0-9.]+)\)", cc_proc.stdout)
        mi_match = re.search(r"([0-9.]+)\s*\(", mi_proc.stdout)
        if cc_avg and mi_match:
            return float(cc_avg.group(1)), float(mi_match.group(1))
    except Exception:
        pass
    finally:
        Path(fname).unlink(missing_ok=True)

    return None


def compute_code_metrics(code: str) -> CodeMetrics:
    m = CodeMetrics()
    if not code.strip():
        return m

    m.lines_of_code = count_lines_of_code(code)

    radon = _try_radon(code)
    if radon:
        m.cyclomatic_complexity, m.maintainability_index = radon
    else:
        m.cyclomatic_complexity = _cc_from_ast(code)
        m.maintainability_index = _mi_from_values(
            code, m.cyclomatic_complexity, m.lines_of_code
        )

    return m
