"""Prompt templates for generating programming tasks."""

KNOWN_PROBLEM_SYSTEM = """You are an expert programming task designer.
You create well-defined algorithmic challenges similar to those found on
LeetCode, HackerRank, and CyberDojo. Always respond in valid JSON."""

KNOWN_PROBLEM_PROMPT = """\
Generate a programming task that is a classic, well-known algorithmic problem.
The task should be solvable in Python and resemble problems from competitive
programming platforms.

Seed: {seed}
Difficulty: {difficulty}

Respond ONLY with a JSON object in exactly this format (no markdown, no prose):
{{
  "title": "short task title",
  "function_signature": "def function_name(param: type) -> return_type:",
  "description": "Clear description of what the function must do.",
  "constraints": "Input/output constraints (size, value ranges, edge cases).",
  "example_inputs": "example_inputs as a Python-readable string",
  "expected_outputs": "expected_outputs as a Python-readable string"
}}
"""

UNKNOWN_PROBLEM_SYSTEM = """You are a creative programming task designer.
You invent novel, unusual programming challenges that are unlikely to appear
in standard algorithm repositories. Respond in valid JSON."""

UNKNOWN_PROBLEM_PROMPT = """\
Invent a novel programming task that is unlikely to exist in any training
dataset. The task should have a clear specification and be solvable in Python,
but should involve an unusual domain or creative combination of concepts.

Seed: {seed}
Domain hint: {domain_hint}
Difficulty: {difficulty_guidance}

Respond ONLY with a JSON object in exactly this format (no markdown, no prose):
{{
  "title": "short task title",
  "function_signature": "def function_name(param: type) -> return_type:",
  "description": "Clear description of what the function must do.",
  "constraints": "Input/output constraints (size, value ranges, edge cases).",
  "example_inputs": "example_inputs as a Python-readable string",
  "expected_outputs": "expected_outputs as a Python-readable string"
}}
"""

DIFFICULTY_GUIDANCE = {
    "medium": (
        "MEDIUM — The solution must be 8-15 lines of Python. "
        "Use only basic building blocks: loops, conditionals, string operations, "
        "simple arithmetic, or basic data structures (list, dict, set). "
        "Do NOT require dynamic programming, graph traversal, recursion, "
        "or any advanced algorithm. A competent programmer solves it in under 20 minutes."
    ),
    "hard": (
        "HARD — The solution should be 15-30 lines of Python. "
        "May use intermediate techniques: sorting with custom keys, two-pointer, "
        "sliding window, simple recursion, or basic DP on a 1D array. "
        "Avoid complex graph algorithms or multi-dimensional DP."
    ),
    "very_hard": (
        "VERY HARD — The solution should be 25-40 lines of Python. "
        "Requires multi-step algorithms: graph traversal (BFS/DFS), "
        "multi-dimensional DP, or complex data structures (heaps, deques). "
        "A strong programmer needs 45+ minutes to solve it correctly."
    ),
    "legendary": (
        "LEGENDARY — The solution should be 40+ lines of Python. "
        "Requires combining multiple advanced techniques, e.g. interval merging with "
        "a heap, topological sort with cycle detection, or segment tree queries. "
        "Only expert programmers solve this without hints."
    ),
    "impossible": (
        "IMPOSSIBLE — Expert-level difficulty. Requires deep algorithmic insight, "
        "e.g. Hierholzer's algorithm for Eulerian paths, suffix arrays, "
        "advanced backtracking with pruning, or non-obvious greedy proofs. "
        "Expect 90+ minutes even for experienced competitive programmers."
    ),
}

DOMAIN_HINTS = [
    "musical rhythms and timing",
    "biological cell automata",
    "warehouse logistics and packing",
    "pixel art encoding",
    "medieval tournament brackets",
    "chemical formula balancing",
    "ancient numeral systems",
    "origami fold sequences",
    "recipe scaling and nutrition",
    "tidal wave simulation",
    "library book sorting rules",
    "traffic light optimization",
]

DIFFICULTIES = ["easy", "medium", "hard"]
