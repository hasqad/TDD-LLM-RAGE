from typing import List, Tuple
import functools

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    @functools.lru_cache(None)
    def dp(recipe_index: int, total_cal: int, total_protein: int) -> int:
        if total_cal >= min_cal and total_protein >= min_protein:
            return 0
        
        cost, (calories, protein) = recipes[recipe_index]
        
        # Include the current recipe
        include_current = cost + dp(recipe_index + 1, total_cal + calories, total_protein + protein)
        
        # Exclude the current recipe if it has no parents or all parents are already considered
        exclude_current = float('inf')
        if not graph[recipe_index] or all(dp(parent, total_cal, total_protein) != float('inf') for parent in graph[recipe_index]):
            exclude_current = dp(recipe_index + 1, total_cal, total_protein)
        
        return min(include_current, exclude_current)
    
    # Start the DP from the first recipe with 0 calories and protein
    return dp(0, 0, 0)

# Example usage:
# print(recipe_chain_optimization(3, [("Recipe1", 10, (5, 5)), ("Recipe2", 20, (10, 10)), ("Recipe3", 30, (15, 15))], [[], [0], [0]], 20, 10))