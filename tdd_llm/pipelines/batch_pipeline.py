"""
Batch TDD pipeline — for one sample.
Generates tests once, generates code once, runs tests. No feedback loop.
"""

import re
import time
from dataclasses import dataclass, field
from typing import Optional

from ..utils.ollama_client import OllamaClient, extract_python_code
from ..prompts.code_prompts import (
    TEST_GENERATION_SYSTEM, TEST_GENERATION_PROMPT,
    CODE_GENERATION_SYSTEM, BATCH_TDD_PROMPT,
)
from ..evaluation.test_runner import run_tests, TestResult


@dataclass
class SampleResult:
    code: str = ""
    tests_code: str = ""
    test_result: Optional[TestResult] = None
    total_attempts: int = 1
    syntax_errors: int = 0
    passed: bool = False
    run_time: float = 0.0
    error: str = ""
    iterations: list = field(default_factory=list)


class BatchPipeline:
    def __init__(self, client: OllamaClient):
        self.client = client

    def generate_tests(self, task: dict, seed: int) -> str:
        fn_name = self._fn_name(task["function_signature"])
        prompt = TEST_GENERATION_PROMPT.format(
            task_description=self._description(task),
            function_signature=task["function_signature"],
            function_name=fn_name,
            example_inputs=task.get("example_inputs", ""),
            expected_outputs=task.get("expected_outputs", ""),
        )
        raw = self.client.generate(
            prompt=prompt, system=TEST_GENERATION_SYSTEM,
            temperature=0.2, seed=seed,
        )
        return extract_python_code(raw)

    def run_sample(self, task: dict, tests_code: str, seed: int) -> SampleResult:
        result = SampleResult(tests_code=tests_code)
        start = time.time()

        prompt = BATCH_TDD_PROMPT.format(
            task_description=self._description(task),
            function_signature=task["function_signature"],
            tests_code=tests_code,
        )
        raw = self.client.generate(
            prompt=prompt, system=CODE_GENERATION_SYSTEM,
            temperature=0.5, seed=seed,
        )
        result.code = extract_python_code(raw)

        try:
            compile(result.code, "solution.py", "exec")
        except SyntaxError as e:
            result.syntax_errors += 1
            result.error = str(e)

        result.test_result = run_tests(result.code, tests_code)
        result.passed = result.test_result.all_passed
        result.run_time = time.time() - start
        return result

    def _fn_name(self, signature: str) -> str:
        m = re.search(r"def\s+(\w+)", signature)
        return m.group(1) if m else "solution"

    def _description(self, task: dict) -> str:
        return (
            f"{task.get('description', '')}\n\n"
            f"Constraints: {task.get('constraints', '')}\n"
            f"Example inputs: {task.get('example_inputs', '')}\n"
            f"Expected outputs: {task.get('expected_outputs', '')}"
        )
