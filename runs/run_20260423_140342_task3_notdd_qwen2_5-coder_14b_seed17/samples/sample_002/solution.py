from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    from functools import lru_cache
    
    @lru_cache(None)
    def dp(recipe_index: int, current_cal: int, current_protein: int) -> int:
        if current_cal >= min_cal and current_protein >= min_protein:
            return 0
        
        name, cost, (calories, protein) = recipes[recipe_index]
        
        # Calculate the minimum cost to meet requirements without this recipe
        min_cost_without = float('inf')
        for parent in graph[recipe_index]:
            min_cost_without = min(min_cost_without, dp(parent, current_cal, current_protein))
        
        # If we include this recipe, add its cost and nutritional values
        if min_cost_without < float('inf'):
            return min(min_cost_without, cost + dp(recipe_index, current_cal + calories, current_protein + protein))
        else:
            return cost + dp(recipe_index, current_cal + calories, current_protein + protein)
    
    # Start from each recipe and find the minimum cost
    total_min_cost = float('inf')
    for i in range(n):
        if not graph[i]:  # Only start from recipes with no parents
            total_min_cost = min(total_min_cost, dp(i, 0, 0))
    
    return total_min_cost if total_min_cost != float('inf') else -1

# Example usage:
# print(recipe_chain_optimization(3, [("Recipe1", 10, (5, 5)), ("Recipe2", 20, (10, 10)), ("Recipe3", 30, (15, 15))], [[], [0], [0]], 20, 10))