from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    def is_valid(state):
        total_cal = sum(recipes[i][2][0] for i in range(n) if state & (1 << i))
        total_protein = sum(recipes[i][2][1] for i in range(n) if state & (1 << i))
        return total_cal >= min_cal and total_protein >= min_protein

    def can_make(state, recipe_index):
        for parent in graph[recipe_index]:
            if not (state & (1 << parent)):
                return False
        return True

    dp = [float('inf')] * (1 << n)
    dp[0] = 0

    for state in range(1 << n):
        for recipe_index in range(n):
            if can_make(state, recipe_index) and not (state & (1 << recipe_index)):
                new_state = state | (1 << recipe_index)
                dp[new_state] = min(dp[new_state], dp[state] + recipes[recipe_index][1])

    result = float('inf')
    for state in range(1 << n):
        if is_valid(state):
            result = min(result, dp[state])

    return result if result != float('inf') else -1