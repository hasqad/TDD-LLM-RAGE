from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    from functools import lru_cache
    
    @lru_cache(None)
    def dp(i, cal, protein):
        if i == n:
            return float('inf') if cal < min_cal or protein < min_protein else 0
        
        cost = recipes[i][1]
        cals = recipes[i][2][0]
        prots = recipes[i][2][1]
        
        # Option 1: Include the current recipe
        include_current = cost + dp(i + 1, cal + cals, protein + prots)
        
        # Option 2: Exclude the current recipe
        exclude_current = float('inf')
        if all(dp(parent, cal, protein) < float('inf') for parent in graph[i]):
            exclude_current = dp(i + 1, cal, protein)
        
        return min(include_current, exclude_current)
    
    return dp(0, 0, 0)