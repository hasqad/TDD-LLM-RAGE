"""Prompt templates for test and code generation."""

TEST_GENERATION_SYSTEM = """You are an expert Python test engineer.
You write correct pytest test suites. Only output valid Python code.
Every assert must have a manually verified expected value — never guess."""

TEST_GENERATION_PROMPT = """\
Write a pytest test suite for the following Python function.

Task:
{task_description}

Function signature:
{function_signature}

Verified examples (these are CORRECT — use them exactly as-is):
Inputs:  {example_inputs}
Outputs: {expected_outputs}

Requirements:
- Use pytest
- The FIRST test MUST assert the exact verified example above — copy it literally
- Add 2-3 more tests for edge cases, but ONLY if you can manually trace through the logic and be 100% certain of the expected value
- If you are not certain of an expected value, DO NOT include that test
- Do NOT test for TypeError, ValueError, or exceptions unless the task explicitly requires it
- Do NOT test behaviour not described in the task
- Each test function must start with test_
- Import the function at the top: from solution import {function_name}
- Do NOT implement the function itself, only tests
- Output ONLY the Python code, no markdown fences
"""

CODE_GENERATION_SYSTEM = """You are an expert Python developer.
You write clean, correct, and efficient Python functions.
Output only valid Python code, no explanations or markdown."""

CODE_GENERATION_PROMPT = """\
Implement the following Python function completely and correctly.

Task:
{task_description}

Function signature:
{function_signature}

Constraints:
{constraints}

Examples:
Inputs:  {example_inputs}
Outputs: {expected_outputs}

Requirements:
- Implement ONLY the function
- Handle all edge cases
- Output ONLY the Python code, no markdown fences
"""

ITERATIVE_FEEDBACK_PROMPT = """\
Your previous implementation failed some tests.

Task:
{task_description}

Function signature:
{function_signature}

Your previous code:
```python
{previous_code}
```

Test failures (attempt {attempt}):
{test_output}

Fix the implementation. Address every failing test.
Output ONLY the corrected Python code, no explanations or markdown fences.
"""

NOTDD_GENERATION_PROMPT = """\
Implement the following Python function completely and correctly.

Task:
{task_description}

Function signature:
{function_signature}

Constraints:
{constraints}

Examples:
Inputs:  {example_inputs}
Outputs: {expected_outputs}

Requirements:
- Implement ONLY the function
- Handle all edge cases
- Output ONLY the Python code, no markdown fences
"""

BATCH_TDD_PROMPT = """\
Implement the following Python function so that it passes all the provided tests.

Task:
{task_description}

Function signature:
{function_signature}

Tests your implementation must pass:
```python
{tests_code}
```

Requirements:
- Implement ONLY the function, not the tests
- Make every test pass
- Output ONLY the Python code, no markdown fences
"""
