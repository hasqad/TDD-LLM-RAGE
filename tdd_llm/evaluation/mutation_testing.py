"""
Mutation testing using AST-based mutations.

Applies simple source-level mutations and checks if the test suite catches them.
"""

import ast
import copy
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MutationResult:
    mutation_score: float = 0.0
    mutants_killed: int = 0
    mutants_total: int = 0
    error: str = ""
    skipped: bool = False


# ---------------------------------------------------------------------------
# AST mutators
# ---------------------------------------------------------------------------

class _ComparisonSwapper(ast.NodeTransformer):
    """Replace each comparison operator with its opposite, one at a time."""
    SWAPS = {
        ast.Lt:    ast.Gt,
        ast.Gt:    ast.Lt,
        ast.LtE:   ast.GtE,
        ast.GtE:   ast.LtE,
        ast.Eq:    ast.NotEq,
        ast.NotEq: ast.Eq,
    }

    def __init__(self, target_index: int):
        self.target = target_index
        self.current = 0
        self.mutated = False

    def visit_Compare(self, node: ast.Compare) -> ast.AST:
        new_ops = []
        for op in node.ops:
            swap = self.SWAPS.get(type(op))
            if swap and self.current == self.target:
                new_ops.append(swap())
                self.mutated = True
            else:
                new_ops.append(op)
            self.current += 1
        node.ops = new_ops
        return self.generic_visit(node)


class _BoolOpSwapper(ast.NodeTransformer):
    """Swap `and` ↔ `or`, one at a time."""

    def __init__(self, target_index: int):
        self.target = target_index
        self.current = 0
        self.mutated = False

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.AST:
        if self.current == self.target:
            self.mutated = True
            node.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
        self.current += 1
        return self.generic_visit(node)


class _ConstantReplacer(ast.NodeTransformer):
    """Replace a numeric constant with constant+1, one at a time."""

    def __init__(self, target_index: int):
        self.target = target_index
        self.current = 0
        self.mutated = False

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            if self.current == self.target:
                self.mutated = True
                return ast.Constant(value=node.value + 1)
            self.current += 1
        return node


class _ReturnNegator(ast.NodeTransformer):
    """Wrap a return expression in `not`, one at a time (booleans only)."""

    def __init__(self, target_index: int):
        self.target = target_index
        self.current = 0
        self.mutated = False

    def visit_Return(self, node: ast.Return) -> ast.AST:
        if node.value is not None:
            if self.current == self.target:
                self.mutated = True
                node.value = ast.UnaryOp(op=ast.Not(), operand=node.value)
            self.current += 1
        return node


def _count_targets(tree: ast.AST, transformer_cls) -> int:
    counter = transformer_cls(target_index=10**9)
    counter.visit(copy.deepcopy(tree))
    return counter.current


def _generate_mutants(source: str) -> list[str]:
    """Return a list of mutated source strings."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    mutants = []
    for transformer_cls in (
        _ComparisonSwapper,
        _BoolOpSwapper,
        _ConstantReplacer,
        _ReturnNegator,
    ):
        n = _count_targets(tree, transformer_cls)
        for i in range(n):
            t = transformer_cls(target_index=i)
            mutated_tree = t.visit(copy.deepcopy(tree))
            if t.mutated:
                try:
                    ast.fix_missing_locations(mutated_tree)
                    mutants.append(ast.unparse(mutated_tree))
                except Exception:
                    pass

    return mutants


# ---------------------------------------------------------------------------
# Test runner for a single mutant
# ---------------------------------------------------------------------------

def _run_tests_on_mutant(
    mutant_code: str,
    test_code: str,
    tmpdir: str,
    timeout: int = 10,
) -> bool:
    """Return True if the test suite KILLS this mutant (tests fail on it)."""
    tmp = Path(tmpdir)
    (tmp / "solution.py").write_text(mutant_code, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "test_solution.py", "-q",
         "--tb=no", "--no-header", "-p", "no:cacheprovider"],
        capture_output=True, text=True,
        timeout=timeout, cwd=tmpdir,
    )
    # Tests fail → mutant killed
    return proc.returncode != 0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def run_mutation_testing(
    solution_code: str,
    test_code: str,
    timeout: int = 300,
) -> MutationResult:
    result = MutationResult()

    mutants = _generate_mutants(solution_code)
    if not mutants:
        result.skipped = True
        result.error = "No mutation sites found in solution."
        return result

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        (tmp / "test_solution.py").write_text(test_code, encoding="utf-8")
        (tmp / "conftest.py").write_text(
            f"import sys\nsys.path.insert(0, r'{tmpdir}')\n", encoding="utf-8"
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = tmpdir

        killed = 0
        per_mutant_timeout = max(10, timeout // max(len(mutants), 1))

        for mutant in mutants:
            try:
                killed += _run_tests_on_mutant(
                    mutant, test_code, tmpdir,
                    timeout=per_mutant_timeout,
                )
            except subprocess.TimeoutExpired:
                killed += 1  # timeout = mutant killed
            except Exception:
                pass

    total = len(mutants)
    result.mutants_killed = killed
    result.mutants_total = total
    result.mutation_score = round(killed / total, 4) if total > 0 else 0.0
    return result
