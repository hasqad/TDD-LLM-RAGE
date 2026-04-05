"""
Test runner — executes pytest test files via subprocess.
"""

import os
import re
import shutil
import subprocess
import sys
import sysconfig
import tempfile
from dataclasses import dataclass
from pathlib import Path

# On macOS with Homebrew, sys.executable resolves to the base Python binary
# (e.g. /opt/homebrew/.../python3.14) which has no venv site-packages.
# sysconfig.get_path("scripts") always returns the active env's bin dir
# (e.g. venv/bin), so venv/bin/pytest uses the venv's Python via its shebang.
def _find_venv_site_packages() -> str | None:
    """Return the site-packages dir of the project venv, or None."""
    for parent in Path(__file__).resolve().parents:
        for name in ("venv", ".venv", "env"):
            lib = parent / name / "lib"
            if lib.is_dir():
                for pyver in lib.iterdir():
                    sp = pyver / "site-packages"
                    if sp.is_dir():
                        return str(sp)
    return None

_VENV_SITE_PACKAGES: str | None = _find_venv_site_packages()
# Always use sys.executable so Python version matches; inject venv site-packages
# via PYTHONPATH so pytest (and the tested code) resolve correctly even when
# the venv's shebang points to a stale path (common after venv moves/copies).
_PYTEST_CMD: list[str] = [sys.executable, "-m", "pytest"]


@dataclass
class TestResult:
    passed: int = 0
    failed: int = 0
    errors: int = 0
    total: int = 0
    output: str = ""
    syntax_error: str = ""

    @property
    def all_passed(self) -> bool:
        return self.total > 0 and self.failed == 0 and self.errors == 0

    @property
    def pass_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.passed / self.total


def run_tests(
    solution_code: str,
    test_code: str,
    timeout: int = 60,
) -> TestResult:
    """
    Write solution and tests to temp files, run pytest via subprocess.
    """
    result = TestResult()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        (tmp / "solution.py").write_text(solution_code, encoding="utf-8")

        # Check syntax of solution
        try:
            compile(solution_code, "solution.py", "exec")
        except SyntaxError as e:
            result.syntax_error = str(e)
            result.output = f"SyntaxError in solution: {e}"
            return result

        (tmp / "test_solution.py").write_text(test_code, encoding="utf-8")

        # Check syntax of tests
        try:
            compile(test_code, "test_solution.py", "exec")
        except SyntaxError as e:
            result.syntax_error = f"SyntaxError in tests: {e}"
            result.output = result.syntax_error
            return result

        # conftest.py ensures tmpdir is on sys.path so
        # "from solution import X" works inside the test file
        (tmp / "conftest.py").write_text(
            f"import sys\nsys.path.insert(0, r'{tmpdir}')\n",
            encoding="utf-8",
        )

        env = os.environ.copy()
        # Prepend venv site-packages so sys.executable (base Python) finds pytest.
        pythonpath_parts = [tmpdir]
        if _VENV_SITE_PACKAGES:
            pythonpath_parts.append(_VENV_SITE_PACKAGES)
        env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

        proc = subprocess.run(
            _PYTEST_CMD + [
                "test_solution.py",
                "--tb=short",
                "-q",
                "--no-header",
                "-p", "no:cacheprovider",
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=tmpdir,
            env=env,
        )

        output = proc.stdout + proc.stderr
        result.output = output

        passed_m = re.search(r"(\d+) passed", output)
        failed_m = re.search(r"(\d+) failed", output)
        error_m  = re.search(r"(\d+) error",  output)

        result.passed = int(passed_m.group(1)) if passed_m else 0
        result.failed = int(failed_m.group(1)) if failed_m else 0
        result.errors = int(error_m.group(1))  if error_m  else 0
        result.total  = result.passed + result.failed + result.errors

        if result.total == 0 and proc.returncode != 0:
            # pytest exit code 5 = no tests collected; treat as "no tests ran" not as an error
            if proc.returncode == 5 or "no tests ran" in output:
                pass  # leave total=0; callers treat empty test suite as no feedback
            else:
                result.errors = 1
                result.total  = 1
                err_match = re.search(r"(E\s+.*(?:Error|error).*)", output)
                if err_match:
                    result.syntax_error = err_match.group(1).strip()

    return result


def count_tests_in_code(test_code: str) -> int:
    return len(re.findall(r"^\s*def test_", test_code, re.MULTILINE))