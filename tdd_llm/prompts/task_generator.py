"""Task generation — uses Ollama to generate programming tasks."""

import json
import random
import re
from pathlib import Path

from ..utils.ollama_client import OllamaClient
from .task_prompts import (
    UNKNOWN_PROBLEM_PROMPT, UNKNOWN_PROBLEM_SYSTEM,
    DOMAIN_HINTS, DIFFICULTY_GUIDANCE,
)

TASK_CACHE_PATH = Path(__file__).parent.parent.parent / "data" / "task_cache.json"


def _load_cache() -> dict:
    if TASK_CACHE_PATH.exists():
        return json.loads(TASK_CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def _save_cache(cache: dict) -> None:
    TASK_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    TASK_CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")

KNOWN_TASKS = [
    {
        "title": "Maximum Subarray Sum",
        "function_signature": "def max_subarray_sum(nums: list[int]) -> int:",
        "description": "Given an array of integers, find the contiguous subarray with the largest sum and return its sum.",
        "constraints": "1 <= len(nums) <= 3*10^4, -10^5 <= nums[i] <= 10^5",
        "example_inputs": "[-2, 1, -3, 4, -1, 2, 1, -5, 4]",
        "expected_outputs": "6",
        "tests_code": """\
from solution import max_subarray_sum

def test_example():
    assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

def test_all_negative():
    assert max_subarray_sum([-3, -1, -2]) == -1

def test_all_positive():
    assert max_subarray_sum([1, 2, 3, 4]) == 10

def test_single_element():
    assert max_subarray_sum([5]) == 5

def test_mixed():
    assert max_subarray_sum([2, -1, 2, -1, 3]) == 5
""",
    },
    {
        "title": "Two Sum",
        "function_signature": "def two_sum(nums: list[int], target: int) -> list[int]:",
        "description": "Given a list of integers and a target, return the indices of the two numbers that add up to the target. Assume exactly one solution exists.",
        "constraints": "2 <= len(nums) <= 10^4, -10^9 <= nums[i] <= 10^9",
        "example_inputs": "[2, 7, 11, 15], 9",
        "expected_outputs": "[0, 1]",
        "tests_code": """\
from solution import two_sum

def test_example():
    assert sorted(two_sum([2, 7, 11, 15], 9)) == [0, 1]

def test_two_elements():
    assert sorted(two_sum([3, 3], 6)) == [0, 1]

def test_negative_numbers():
    assert sorted(two_sum([-1, -2, -3, -4, -5], -8)) == [2, 4]

def test_larger_list():
    result = two_sum([1, 5, 3, 7, 9, 2], 12)
    assert sorted(result) == [1, 4]

def test_zeros():
    assert sorted(two_sum([0, 4, 3, 0], 0)) == [0, 3]
""",
    },
    {
        "title": "Valid Parentheses",
        "function_signature": "def is_valid(s: str) -> bool:",
        "description": "Given a string containing only '(', ')', '{', '}', '[', ']', determine if the input string is valid. Open brackets must be closed by the same type in the correct order.",
        "constraints": "1 <= len(s) <= 10^4, s consists only of parentheses characters",
        "example_inputs": "'()[]{}'",
        "expected_outputs": "True",
        "tests_code": """\
from solution import is_valid

def test_example():
    assert is_valid('()[]{}') is True

def test_nested():
    assert is_valid('({[]})') is True

def test_wrong_order():
    assert is_valid('([)]') is False

def test_unclosed():
    assert is_valid('(') is False

def test_only_closes():
    assert is_valid(')') is False

def test_empty():
    assert is_valid('') is True
""",
    },
    {
        "title": "Fibonacci Number",
        "function_signature": "def fib(n: int) -> int:",
        "description": "Return the n-th Fibonacci number where fib(0)=0 and fib(1)=1.",
        "constraints": "0 <= n <= 30",
        "example_inputs": "10",
        "expected_outputs": "55",
        "tests_code": """\
from solution import fib

def test_example():
    assert fib(10) == 55

def test_base_case_0():
    assert fib(0) == 0

def test_base_case_1():
    assert fib(1) == 1

def test_small():
    assert fib(5) == 5

def test_larger():
    assert fib(15) == 610
""",
    },
    {
        "title": "Palindrome Check",
        "function_signature": "def is_palindrome(s: str) -> bool:",
        "description": "Given a string, return True if it reads the same forwards and backwards (case-insensitive, ignoring non-alphanumeric characters).",
        "constraints": "0 <= len(s) <= 2*10^5",
        "example_inputs": "'A man a plan a canal Panama'",
        "expected_outputs": "True",
        "tests_code": """\
from solution import is_palindrome

def test_example():
    assert is_palindrome('A man a plan a canal Panama') is True

def test_simple_palindrome():
    assert is_palindrome('racecar') is True

def test_not_palindrome():
    assert is_palindrome('hello') is False

def test_with_punctuation():
    assert is_palindrome('Was it a car or a cat I saw?') is True

def test_single_char():
    assert is_palindrome('a') is True

def test_empty():
    assert is_palindrome('') is True
""",
    },
    {
        "title": "Merge Sorted Arrays",
        "function_signature": "def merge_sorted(a: list[int], b: list[int]) -> list[int]:",
        "description": "Merge two sorted lists into a single sorted list.",
        "constraints": "0 <= len(a), len(b) <= 10^4",
        "example_inputs": "[1, 3, 5], [2, 4, 6]",
        "expected_outputs": "[1, 2, 3, 4, 5, 6]",
        "tests_code": """\
from solution import merge_sorted

def test_example():
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

def test_one_empty():
    assert merge_sorted([], [1, 2, 3]) == [1, 2, 3]

def test_both_empty():
    assert merge_sorted([], []) == []

def test_duplicates():
    assert merge_sorted([1, 2, 2], [2, 3]) == [1, 2, 2, 2, 3]

def test_different_lengths():
    assert merge_sorted([1], [2, 3, 4, 5]) == [1, 2, 3, 4, 5]
""",
    },
    {
        "title": "Reverse List",
        "function_signature": "def reverse_list(nums: list[int]) -> list[int]:",
        "description": "Given a list of integers, return the list reversed.",
        "constraints": "0 <= len(nums) <= 5000",
        "example_inputs": "[1, 2, 3, 4, 5]",
        "expected_outputs": "[5, 4, 3, 2, 1]",
        "tests_code": """\
from solution import reverse_list

def test_example():
    assert reverse_list([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1]

def test_empty():
    assert reverse_list([]) == []

def test_single():
    assert reverse_list([42]) == [42]

def test_negatives():
    assert reverse_list([-1, -2, -3]) == [-3, -2, -1]

def test_mixed():
    assert reverse_list([1, -2, 3, -4]) == [-4, 3, -2, 1]
""",
    },
    {
        "title": "Climbing Stairs",
        "function_signature": "def climb_stairs(n: int) -> int:",
        "description": "You are climbing a staircase with n steps. Each time you can climb 1 or 2 steps. Return the number of distinct ways to reach the top.",
        "constraints": "1 <= n <= 45",
        "example_inputs": "5",
        "expected_outputs": "8",
        "tests_code": """\
from solution import climb_stairs

def test_example():
    assert climb_stairs(5) == 8

def test_one_step():
    assert climb_stairs(1) == 1

def test_two_steps():
    assert climb_stairs(2) == 2

def test_three_steps():
    assert climb_stairs(3) == 3

def test_larger():
    assert climb_stairs(10) == 89
""",
    },
    {
        "title": "Decode Ways",
        "function_signature": "def num_decodings(s: str) -> int:",
        "description": (
            "A string of digits can be decoded where 'A'=1, 'B'=2, ..., 'Z'=26. "
            "Return the number of ways to decode the string. "
            "Digits with a leading zero (e.g. '06') are not valid two-digit encodings. "
            "A single '0' cannot be decoded."
        ),
        "constraints": "1 <= len(s) <= 100, s contains only digits",
        "example_inputs": "'226'",
        "expected_outputs": "3",
        "tests_code": """\
from solution import num_decodings

def test_example():
    # "226" -> "BZ"(2,26), "VF"(22,6), "BBF"(2,2,6) -> 3 ways
    assert num_decodings("226") == 3

def test_single_zero():
    assert num_decodings("0") == 0

def test_leading_zero():
    assert num_decodings("06") == 0

def test_ten():
    # "10" -> "J"(10) only -> 1 way
    assert num_decodings("10") == 1

def test_single_digit():
    assert num_decodings("7") == 1

def test_complex():
    # "11106" -> "AAJF"(1,1,10,6), "KJF"(11,10,6) -> 2 ways
    assert num_decodings("11106") == 2
""",
    },
    {
        "title": "Spiral Matrix",
        "function_signature": "def spiral_order(matrix: list[list[int]]) -> list[int]:",
        "description": (
            "Given an m x n matrix, return all elements in spiral order "
            "(clockwise from the top-left: go right, then down, then left, then up, repeat)."
        ),
        "constraints": "m == len(matrix), n == len(matrix[0]), 1 <= m, n <= 10, -100 <= matrix[i][j] <= 100",
        "example_inputs": "[[1,2,3],[4,5,6],[7,8,9]]",
        "expected_outputs": "[1,2,3,6,9,8,7,4,5]",
        "tests_code": """\
from solution import spiral_order

def test_3x3():
    assert spiral_order([[1,2,3],[4,5,6],[7,8,9]]) == [1,2,3,6,9,8,7,4,5]

def test_single_row():
    assert spiral_order([[1,2,3,4]]) == [1,2,3,4]

def test_single_col():
    assert spiral_order([[1],[2],[3]]) == [1,2,3]

def test_single_element():
    assert spiral_order([[42]]) == [42]

def test_2x2():
    assert spiral_order([[1,2],[3,4]]) == [1,2,4,3]

def test_3x4():
    assert spiral_order([[1,2,3,4],[5,6,7,8],[9,10,11,12]]) == [1,2,3,4,8,12,11,10,9,5,6,7]
""",
    },
    {
        "title": "Unique Paths with Obstacles",
        "function_signature": "def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:",
        "description": (
            "A robot on an m x n grid starts at the top-left corner and wants to reach the bottom-right. "
            "It can only move right or down. Some cells have obstacles (marked 1), free cells are 0. "
            "Return the number of unique paths from start to end. "
            "Return 0 if start or end is blocked."
        ),
        "constraints": "m == len(obstacle_grid), n == len(obstacle_grid[0]), 1 <= m, n <= 100",
        "example_inputs": "[[0,0,0],[0,1,0],[0,0,0]]",
        "expected_outputs": "2",
        "tests_code": """\
from solution import unique_paths_with_obstacles

def test_example():
    assert unique_paths_with_obstacles([[0,0,0],[0,1,0],[0,0,0]]) == 2

def test_blocked_start():
    assert unique_paths_with_obstacles([[1,0],[0,0]]) == 0

def test_blocked_end():
    assert unique_paths_with_obstacles([[0,0],[0,1]]) == 0

def test_no_obstacles():
    assert unique_paths_with_obstacles([[0,0,0],[0,0,0]]) == 3

def test_single_row():
    assert unique_paths_with_obstacles([[0,0,1,0]]) == 0

def test_single_cell_free():
    assert unique_paths_with_obstacles([[0]]) == 1
""",
    },
    # ------------------------------------------------------------------ VERY HARD
    {
        "title": "Trapping Rain Water",
        "function_signature": "def trap(height: list[int]) -> int:",
        "description": (
            "Given n non-negative integers representing an elevation map where the width of each bar is 1, "
            "compute how much water it can trap after raining."
        ),
        "constraints": "n == len(height), 1 <= n <= 2*10^4, 0 <= height[i] <= 10^5",
        "example_inputs": "[0,1,0,2,1,0,1,3,2,1,2,1]",
        "expected_outputs": "6",
        "tests_code": """\
from solution import trap

def test_example():
    assert trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6

def test_simple():
    assert trap([4,2,0,3,2,5]) == 9

def test_no_water():
    assert trap([1,2,3,4,5]) == 0

def test_single():
    assert trap([3]) == 0

def test_two_bars():
    assert trap([3,0,2]) == 2

def test_flat():
    assert trap([0,0,0]) == 0
""",
    },
    {
        "title": "Edit Distance",
        "function_signature": "def min_distance(word1: str, word2: str) -> int:",
        "description": (
            "Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2. "
            "You have three operations: insert a character, delete a character, replace a character."
        ),
        "constraints": "0 <= len(word1), len(word2) <= 500",
        "example_inputs": "'horse', 'ros'",
        "expected_outputs": "3",
        "tests_code": """\
from solution import min_distance

def test_example():
    assert min_distance('horse', 'ros') == 3

def test_intention_execution():
    assert min_distance('intention', 'execution') == 5

def test_empty_to_word():
    assert min_distance('', 'abc') == 3

def test_word_to_empty():
    assert min_distance('abc', '') == 3

def test_same_word():
    assert min_distance('abc', 'abc') == 0

def test_single_chars():
    assert min_distance('a', 'b') == 1
""",
    },
    {
        "title": "Word Break",
        "function_signature": "def word_break(s: str, wordDict: list[str]) -> bool:",
        "description": (
            "Given a string s and a dictionary of strings wordDict, return True if s can be segmented into "
            "a space-separated sequence of one or more dictionary words. Words in the dictionary may be reused."
        ),
        "constraints": "1 <= len(s) <= 300, 1 <= len(wordDict) <= 1000, wordDict entries consist of lowercase English letters",
        "example_inputs": "'leetcode', ['leet', 'code']",
        "expected_outputs": "True",
        "tests_code": """\
from solution import word_break

def test_example():
    assert word_break('leetcode', ['leet', 'code']) is True

def test_applepenapple():
    assert word_break('applepenapple', ['apple', 'pen']) is True

def test_catsandog():
    assert word_break('catsandog', ['cats', 'dog', 'sand', 'and', 'cat']) is False

def test_single_word():
    assert word_break('dog', ['dog']) is True

def test_not_found():
    assert word_break('abc', ['ab', 'xyz']) is False

def test_reuse():
    assert word_break('aaa', ['a', 'aa']) is True
""",
    },
    # --------------------------------------------------------------- EXTREMELY HARD
    {
        "title": "Regular Expression Matching",
        "function_signature": "def is_match(s: str, p: str) -> bool:",
        "description": (
            "Given an input string s and a pattern p, implement regular expression matching with '.' and '*'. "
            "'.' matches any single character. "
            "'*' matches zero or more of the preceding element. "
            "The matching must cover the entire string (not partial)."
        ),
        "constraints": "1 <= len(s) <= 20, 1 <= len(p) <= 30, s contains only lowercase letters, p contains only lowercase letters, '.', and '*'",
        "example_inputs": "'aa', 'a*'",
        "expected_outputs": "True",
        "tests_code": """\
from solution import is_match

def test_star_repetition():
    assert is_match('aa', 'a*') is True

def test_dot_star():
    assert is_match('ab', '.*') is True

def test_complex():
    assert is_match('aab', 'c*a*b') is True

def test_no_match():
    assert is_match('aa', 'a') is False

def test_empty_pattern_star():
    assert is_match('mississippi', 'mis*is*p*.') is False

def test_empty_string():
    assert is_match('', '.*') is True

def test_dot_match():
    assert is_match('abc', 'a.c') is True
""",
    },
    {
        "title": "Median of Two Sorted Arrays",
        "function_signature": "def find_median_sorted_arrays(nums1: list[int], nums2: list[int]) -> float:",
        "description": (
            "Given two sorted arrays nums1 and nums2, return the median of the two sorted arrays. "
            "The overall run time complexity should be O(log(m+n))."
        ),
        "constraints": "0 <= len(nums1), len(nums2) <= 1000, -10^6 <= nums1[i], nums2[i] <= 10^6, nums1 and nums2 are sorted in non-decreasing order",
        "example_inputs": "[1,3], [2]",
        "expected_outputs": "2.0",
        "tests_code": """\
from solution import find_median_sorted_arrays

def test_odd_total():
    assert find_median_sorted_arrays([1,3], [2]) == 2.0

def test_even_total():
    assert find_median_sorted_arrays([1,2], [3,4]) == 2.5

def test_one_empty():
    assert find_median_sorted_arrays([], [1]) == 1.0

def test_both_single():
    assert find_median_sorted_arrays([1], [2]) == 1.5

def test_disjoint():
    assert find_median_sorted_arrays([1,2,3], [4,5,6]) == 3.5

def test_duplicates():
    assert find_median_sorted_arrays([1,1], [1,1]) == 1.0
""",
    },
    {
        "title": "N-Queens",
        "function_signature": "def solve_n_queens(n: int) -> list[list[str]]:",
        "description": (
            "The n-queens puzzle places n queens on an n x n chessboard so that no two queens attack each other. "
            "Return all distinct solutions. Each solution is a list of n strings, each of length n, "
            "using 'Q' for a queen and '.' for an empty cell."
        ),
        "constraints": "1 <= n <= 9",
        "example_inputs": "4",
        "expected_outputs": "2 solutions",
        "tests_code": """\
from solution import solve_n_queens

def test_n1():
    assert solve_n_queens(1) == [['Q']]

def test_n2_no_solution():
    assert solve_n_queens(2) == []

def test_n3_no_solution():
    assert solve_n_queens(3) == []

def test_n4_count():
    assert len(solve_n_queens(4)) == 2

def test_n5_count():
    assert len(solve_n_queens(5)) == 10

def test_n4_valid():
    solutions = solve_n_queens(4)
    for sol in solutions:
        assert len(sol) == 4
        assert all(len(row) == 4 for row in sol)
        assert sum(row.count('Q') for row in sol) == 4
""",
    },
    # ------------------------------------------------------------------- LEGENDARY
    {
        "title": "Burst Balloons",
        "function_signature": "def max_coins(nums: list[int]) -> int:",
        "description": (
            "You are given n balloons indexed from 0 to n-1. Each balloon has a number on it. "
            "If you burst balloon i, you gain nums[i-1] * nums[i] * nums[i+1] coins. "
            "Balloons out of bounds are treated as having value 1. "
            "Return the maximum coins you can collect by bursting all balloons."
        ),
        "constraints": "1 <= n <= 300, 0 <= nums[i] <= 100",
        "example_inputs": "[3,1,5,8]",
        "expected_outputs": "167",
        "tests_code": """\
from solution import max_coins

def test_example():
    assert max_coins([3,1,5,8]) == 167

def test_single():
    assert max_coins([5]) == 5

def test_two():
    assert max_coins([3,5]) == 30

def test_zeros():
    assert max_coins([0,0,0]) == 0

def test_ones():
    assert max_coins([1,1,1]) == 4

def test_increasing():
    assert max_coins([1,2,3,4]) == 20
""",
    },
    {
        "title": "Largest Rectangle in Histogram",
        "function_signature": "def largest_rectangle_area(heights: list[int]) -> int:",
        "description": (
            "Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, "
            "return the area of the largest rectangle in the histogram."
        ),
        "constraints": "1 <= len(heights) <= 10^5, 0 <= heights[i] <= 10^4",
        "example_inputs": "[2,1,5,6,2,3]",
        "expected_outputs": "10",
        "tests_code": """\
from solution import largest_rectangle_area

def test_example():
    assert largest_rectangle_area([2,1,5,6,2,3]) == 10

def test_single():
    assert largest_rectangle_area([5]) == 5

def test_ascending():
    assert largest_rectangle_area([1,2,3,4,5]) == 9

def test_descending():
    assert largest_rectangle_area([5,4,3,2,1]) == 9

def test_all_same():
    assert largest_rectangle_area([3,3,3]) == 9

def test_with_zero():
    assert largest_rectangle_area([2,0,2]) == 2
""",
    },
    {
        "title": "Minimum Window Substring",
        "function_signature": "def min_window(s: str, t: str) -> str:",
        "description": (
            "Given two strings s and t, return the minimum window substring of s such that every character in t "
            "(including duplicates) is included in the window. "
            "If there is no such substring, return an empty string. "
            "The answer is guaranteed to be unique."
        ),
        "constraints": "1 <= len(s), len(t) <= 10^5, s and t consist of uppercase and lowercase English letters",
        "example_inputs": "'ADOBECODEBANC', 'ABC'",
        "expected_outputs": "'BANC'",
        "tests_code": """\
from solution import min_window

def test_example():
    assert min_window('ADOBECODEBANC', 'ABC') == 'BANC'

def test_no_window():
    assert min_window('a', 'aa') == ''

def test_exact_match():
    assert min_window('a', 'a') == 'a'

def test_duplicates_in_t():
    assert min_window('aa', 'aa') == 'aa'

def test_full_string():
    assert min_window('abc', 'abc') == 'abc'

def test_single_char():
    assert min_window('ADOBECODEBANC', 'A') == 'A'
""",
    },
    {
        "title": "Count of Smaller Numbers After Self",
        "function_signature": "def count_smaller(nums: list[int]) -> list[int]:",
        "description": (
            "Given an integer array nums, return an integer array counts where counts[i] is the number of smaller "
            "elements to the right of nums[i]."
        ),
        "constraints": "1 <= len(nums) <= 10^5, -10^4 <= nums[i] <= 10^4",
        "example_inputs": "[5,2,6,1]",
        "expected_outputs": "[2,1,1,0]",
        "tests_code": """\
from solution import count_smaller

def test_example():
    assert count_smaller([5,2,6,1]) == [2,1,1,0]

def test_single():
    assert count_smaller([1]) == [0]

def test_ascending():
    assert count_smaller([1,2,3]) == [0,0,0]

def test_descending():
    assert count_smaller([3,2,1]) == [2,1,0]

def test_duplicates():
    assert count_smaller([2,0,1]) == [2,1,0]

def test_all_same():
    assert count_smaller([1,1,1]) == [0,0,0]
""",
    },
    # ------------------------------------------------------------------- IMPOSSIBLE
    {
        "title": "Alien Dictionary",
        "function_signature": "def alien_order(words: list[str]) -> str:",
        "description": (
            "There is a new alien language that uses the English alphabet. However, the order of the letters is unknown. "
            "You are given a list of strings words from the alien language's dictionary, where the strings are sorted "
            "lexicographically by the rules of this new language. "
            "Derive the order of letters in this language and return it as a string. "
            "If no valid order exists, return ''. If multiple valid orders exist, return any of them."
        ),
        "constraints": "1 <= len(words) <= 100, 1 <= len(words[i]) <= 100, words[i] consists of lowercase English letters",
        "example_inputs": '["wrt","wrf","er","ett","rftt"]',
        "expected_outputs": '"wertf"',
        "tests_code": """\
from solution import alien_order

def test_example():
    result = alien_order(['wrt','wrf','er','ett','rftt'])
    # verify topological order is consistent
    assert set(result) == {'w','e','r','t','f'}

def test_single_word():
    result = alien_order(['abc'])
    assert set(result) == {'a','b','c'}

def test_invalid():
    assert alien_order(['abc','ab']) == ''

def test_two_words():
    result = alien_order(['z','x'])
    assert result.index('z') < result.index('x')

def test_no_ordering():
    result = alien_order(['a','b','c'])
    assert set(result) == {'a','b','c'}

def test_cycle():
    assert alien_order(['a','b','a']) == ''
""",
    },
    {
        "title": "Sliding Window Maximum",
        "function_signature": "def max_sliding_window(nums: list[int], k: int) -> list[int]:",
        "description": (
            "You are given an array of integers nums and an integer k. "
            "There is a sliding window of size k moving from left to right. "
            "You can only see the k numbers in the window. "
            "Return the max sliding window — the maximum value in each window position."
        ),
        "constraints": "1 <= len(nums) <= 10^5, -10^4 <= nums[i] <= 10^4, 1 <= k <= len(nums)",
        "example_inputs": "[1,3,-1,-3,5,3,6,7], 3",
        "expected_outputs": "[3,3,5,5,6,7]",
        "tests_code": """\
from solution import max_sliding_window

def test_example():
    assert max_sliding_window([1,3,-1,-3,5,3,6,7], 3) == [3,3,5,5,6,7]

def test_k_equals_length():
    assert max_sliding_window([1,3,2], 3) == [3]

def test_k_equals_one():
    assert max_sliding_window([4,3,2,1], 1) == [4,3,2,1]

def test_all_same():
    assert max_sliding_window([2,2,2,2], 2) == [2,2,2]

def test_descending():
    assert max_sliding_window([5,4,3,2,1], 2) == [5,4,3,2]

def test_single():
    assert max_sliding_window([7], 1) == [7]
""",
    },
    {
        "title": "Reconstruct Itinerary",
        "function_signature": "def find_itinerary(tickets: list[list[str]]) -> list[str]:",
        "description": (
            "You are given a list of airline tickets represented by pairs [from, to]. "
            "Reconstruct the itinerary in order. All tickets must be used. "
            "The itinerary must begin with 'JFK'. "
            "If multiple valid itineraries exist, return the one with the smallest lexical order."
        ),
        "constraints": "1 <= len(tickets) <= 300, tickets[i].length == 2, from_i and to_i consist of uppercase English letters, from_i != to_i",
        "example_inputs": '[["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]',
        "expected_outputs": '["JFK","MUC","LHR","SFO","SJC"]',
        "tests_code": """\
from solution import find_itinerary

def test_example():
    tickets = [['MUC','LHR'],['JFK','MUC'],['SFO','SJC'],['LHR','SFO']]
    assert find_itinerary(tickets) == ['JFK','MUC','LHR','SFO','SJC']

def test_lexical_order():
    tickets = [['JFK','SFO'],['JFK','ATL'],['SFO','ATL'],['ATL','JFK'],['ATL','SFO']]
    assert find_itinerary(tickets) == ['JFK','ATL','JFK','SFO','ATL','SFO']

def test_single_ticket():
    assert find_itinerary([['JFK','LAX']]) == ['JFK','LAX']

def test_cycle():
    tickets = [['JFK','ATL'],['ATL','JFK']]
    assert find_itinerary(tickets) == ['JFK','ATL','JFK']
""",
    },
]


class TaskGenerator:
    def __init__(self, client: OllamaClient):
        self.client = client

    def generate_known(self, seed: int = 0) -> dict:
        rng = random.Random(seed)
        task = rng.choice(KNOWN_TASKS).copy()
        task["source"] = "known"
        task["seed"] = seed
        return task

    def generate_unknown(self, seed: int = 0, difficulty: str = "medium") -> dict:
        cache_key = f"{seed}_{difficulty}"
        cache = _load_cache()
        if cache_key in cache:
            print(f"[TaskCache] Loaded task for seed={seed} difficulty={difficulty}")
            return cache[cache_key]

        rng = random.Random(seed)
        domain_hint = rng.choice(DOMAIN_HINTS)
        difficulty_guidance = DIFFICULTY_GUIDANCE.get(difficulty, DIFFICULTY_GUIDANCE["medium"])
        prompt = UNKNOWN_PROBLEM_PROMPT.format(
            seed=seed, domain_hint=domain_hint, difficulty_guidance=difficulty_guidance
        )

        last_error = None
        for attempt in range(3):
            try:
                response = self.client.generate(
                    prompt=prompt, system=UNKNOWN_PROBLEM_SYSTEM,
                    temperature=0.7, seed=seed + attempt,
                )
                task = self._parse_task(response, source="unknown", seed=seed)
                cache[cache_key] = task
                _save_cache(cache)
                print(f"[TaskCache] Saved task for seed={seed} difficulty={difficulty}")
                return task
            except (ValueError, Exception) as e:
                last_error = e
                print(f"[TaskCache] Attempt {attempt+1}/3 failed: {e}")

        raise ValueError(f"Task generation failed after 3 attempts: {last_error}")

    def _parse_task(self, response: str, source: str, seed: int) -> dict:
        text = response.strip()
        if text.startswith("```"):
            text = "\n".join(
                l for l in text.split("\n")
                if not l.strip().startswith("```")
            ).strip()
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
            else:
                raise ValueError(
                    f"Could not parse task JSON:\n{response[:500]}"
                )
        return {
            "source": source,
            "seed": seed,
            "title": data.get("title", "Untitled"),
            "function_signature": data.get("function_signature", "def solution():"),
            "description": data.get("description", ""),
            "constraints": data.get("constraints", ""),
            "example_inputs": data.get("example_inputs", ""),
            "expected_outputs": data.get("expected_outputs", ""),
        }

    def build_full_description(self, task: dict) -> str:
        return (
            f"Title: {task['title']}\n\n"
            f"Description:\n{task['description']}\n\n"
            f"Function Signature:\n{task['function_signature']}\n\n"
            f"Constraints:\n{task['constraints']}\n\n"
            f"Example Inputs:\n{task['example_inputs']}\n\n"
            f"Expected Outputs:\n{task['expected_outputs']}\n"
        )
