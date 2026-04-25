from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    from functools import lru_cache
    
    @lru_cache(None)
    def dp(i: int, cal: int, protein: int) -> int:
        if i == n:
            return float('inf') if cal < min_cal or protein < min_protein else 0
        
        # Skip the current recipe
        skip_cost = dp(i + 1, cal, protein)
        
        # Include the current recipe if all its parents are included
        include_cost = float('inf')
        can_include = True
        for parent in graph[i]:
            if dp(parent, 0, 0) == float('inf'):
                can_include = False
                break
        
        if can_include:
            name, cost, (cals, prots) = recipes[i]
            include_cost = cost + dp(i + 1, cal + cals, protein + prots)
        
        return min(skip_cost, include_cost)
    
    return dp(0, 0, 0)

# Example usage:
# print(recipe_chain_optimization(3, [("Recipe1", 10, (5, 5)), ("Recipe2", 20, (10, 10)), ("Recipe3", 30, (15, 15))], [[], [0], [0]], 20, 10))