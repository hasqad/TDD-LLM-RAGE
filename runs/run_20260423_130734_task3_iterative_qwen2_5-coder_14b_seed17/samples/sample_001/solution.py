from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    from functools import lru_cache
    
    @lru_cache(None)
    def dp(i: int, cal: int, protein: int) -> int:
        if i == n:
            return 0 if cal >= min_cal and protein >= min_protein else float('inf')
        
        # Check dependencies
        for parent in graph[i]:
            if dp(parent, cal, protein) == float('inf'):
                return float('inf')
        
        # Option to skip the current recipe
        skip = dp(i + 1, cal, protein)
        
        # Option to include the current recipe
        _, cost, (cals, prots) = recipes[i]
        include = cost + dp(i + 1, cal + cals, protein + prots)
        
        return min(skip, include)
    
    # Start from the first recipe with initial calorie and protein values of 0
    result = dp(0, 0, 0)
    
    # Check if it's possible to meet the minimum requirements
    return result if result != float('inf') else -1

# Example usage:
# print(recipe_chain_optimization(3, [("Recipe1", 10, (5, 5)), ("Recipe2", 20, (10, 10)), ("Recipe3", 30, (15, 15))], [[], [0], [0]], 20, 10))