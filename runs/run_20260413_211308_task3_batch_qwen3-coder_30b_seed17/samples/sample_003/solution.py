from typing import List, Tuple
from functools import lru_cache

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Preprocess recipes into a more convenient format
    recipe_data = []
    for name, cost, (calories, protein) in recipes:
        recipe_data.append((cost, calories, protein))
    
    # Memoization for dynamic programming
    @lru_cache(maxsize=None)
    def dp(mask, cal, prot):
        # Base case: if we've met the requirements
        if cal >= min_cal and prot >= min_protein:
            return 0
        
        # If we've considered all recipes
        if mask == (1 << n) - 1:
            return float('inf')
        
        min_cost = float('inf')
        
        # Try adding each recipe that hasn't been added yet
        for i in range(n):
            # If recipe i is already included
            if mask & (1 << i):
                continue
            
            # Check if all dependencies are satisfied
            can_include = True
            for parent in graph[i]:
                if not (mask & (1 << parent)):
                    can_include = False
                    break
            
            if not can_include:
                continue
            
            # Add recipe i and recurse
            new_mask = mask | (1 << i)
            cost, calories, protein = recipe_data[i]
            new_cal = cal + calories
            new_prot = prot + protein
            
            result = dp(new_mask, new_cal, new_prot)
            if result != float('inf'):
                min_cost = min(min_cost, cost + result)
        
        return min_cost
    
    # Start with no recipes selected
    result = dp(0, 0, 0)
    return result if result != float('inf') else -1