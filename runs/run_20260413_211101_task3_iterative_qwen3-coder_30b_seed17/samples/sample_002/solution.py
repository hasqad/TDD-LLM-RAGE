from typing import List, Tuple
from functools import lru_cache

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Convert graph to list of sets for easier lookup
    parent_sets = [set(parents) for parents in graph]
    
    # Memoization cache
    @lru_cache(maxsize=None)
    def dp(mask):
        # Calculate total calories, protein and cost for current selection
        total_cal = 0
        total_protein = 0
        total_cost = 0
        
        for i in range(n):
            if mask & (1 << i):
                recipe = recipes[i]
                total_cal += recipe[2][0]
                total_protein += recipe[2][1]
                total_cost += recipe[1]
        
        # Check if we meet the requirements
        if total_cal >= min_cal and total_protein >= min_protein:
            return total_cost
        
        # Try adding each recipe that can be added (no dependency violations)
        min_cost = float('inf')
        for i in range(n):
            # Skip if already selected
            if mask & (1 << i):
                continue
            
            # Check if all parents are selected
            can_add = True
            for parent in parent_sets[i]:
                if not (mask & (1 << parent)):
                    can_add = False
                    break
            
            if can_add:
                new_mask = mask | (1 << i)
                cost = dp(new_mask)
                min_cost = min(min_cost, cost)
        
        return min_cost if min_cost != float('inf') else float('inf')
    
    # Try all possible combinations starting with each recipe
    result = float('inf')
    for i in range(n):
        # Check if we can start with this recipe (no dependencies)
        if not parent_sets[i]:  # No parents
            cost = dp(1 << i)
            result = min(result, cost)
    
    # If no valid solution found, return -1 or handle as needed
    return result if result != float('inf') else -1