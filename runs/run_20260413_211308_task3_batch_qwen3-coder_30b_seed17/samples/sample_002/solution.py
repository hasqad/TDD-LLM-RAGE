from typing import List, Tuple
from functools import lru_cache

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Preprocess recipes to make them easier to work with
    recipe_data = []
    for name, cost, (calories, protein) in recipes:
        recipe_data.append((cost, calories, protein))
    
    # Memoization for dynamic programming
    @lru_cache(maxsize=None)
    def dp(mask):
        # mask represents which recipes are selected (bitmask)
        total_cost = 0
        total_cal = 0
        total_protein = 0
        
        # Calculate totals for current selection
        for i in range(n):
            if mask & (1 << i):
                cost, cal, prot = recipe_data[i]
                total_cost += cost
                total_cal += cal
                total_protein += prot
        
        # Check if we meet the requirements
        if total_cal >= min_cal and total_protein >= min_protein:
            return total_cost
        
        # Try adding each recipe that can be added (no dependencies violated)
        min_cost = float('inf')
        for i in range(n):
            if not (mask & (1 << i)):  # If recipe i is not selected
                # Check if all dependencies are satisfied
                can_add = True
                for parent in graph[i]:
                    if not (mask & (1 << parent)):  # Parent not selected
                        can_add = False
                        break
                
                if can_add:
                    new_mask = mask | (1 << i)
                    result = dp(new_mask)
                    min_cost = min(min_cost, result)
        
        return min_cost if min_cost != float('inf') else float('inf')
    
    # Try all possible combinations starting with each recipe
    result = float('inf')
    
    # Try starting with each recipe individually
    for i in range(n):
        # Check if we can start with this recipe (no dependencies)
        can_start = True
        for parent in graph[i]:
            if parent >= n or parent < 0:  # Invalid parent
                can_start = False
                break
        
        if can_start:
            new_mask = 1 << i
            result = min(result, dp(new_mask))
    
    # Also try combinations of recipes that don't depend on anything else
    # This handles cases where we need to select multiple recipes
    # We'll use a different approach - try all subsets that satisfy dependencies
    
    # Generate all valid combinations using bitmasks
    def is_valid_subset(mask):
        # Check if all dependencies are satisfied
        for i in range(n):
            if mask & (1 << i):  # If recipe i is selected
                for parent in graph[i]:
                    if not (mask & (1 << parent)):  # Parent not selected
                        return False
        return True
    
    def get_totals(mask):
        total_cost = 0
        total_cal = 0
        total_protein = 0
        for i in range(n):
            if mask & (1 << i):
                cost, cal, prot = recipe_data[i]
                total_cost += cost
                total_cal += cal
                total_protein += prot
        return total_cost, total_cal, total_protein
    
    # Try all possible combinations
    min_total = float('inf')
    
    # Generate all possible combinations
    for mask in range(1 << n):
        if is_valid_subset(mask):
            cost, cal, prot = get_totals(mask)
            if cal >= min_cal and prot >= min_protein:
                min_total = min(min_total, cost)
    
    return min_total if min_total != float('inf') else -1