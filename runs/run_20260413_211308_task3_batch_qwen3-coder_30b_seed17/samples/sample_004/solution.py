from typing import List, Tuple
from functools import lru_cache

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Precompute all possible combinations of recipes that satisfy the constraints
    # Use bitmask to represent which recipes are selected
    INF = float('inf')
    
    # Convert graph to a more usable format
    # graph[i] contains the indices of recipes that must be selected before recipe i
    # We need to find all valid combinations of recipes that satisfy dependencies
    
    # For each subset of recipes, check if it's valid (all dependencies satisfied)
    # and if it meets the nutritional requirements
    
    min_cost = INF
    
    # Try all possible combinations of recipes (2^n combinations)
    for mask in range(1 << n):
        # Check if dependencies are satisfied
        valid = True
        total_cal = 0
        total_protein = 0
        total_cost = 0
        
        for i in range(n):
            if mask & (1 << i):  # Recipe i is selected
                # Check if all dependencies are satisfied
                for parent in graph[i]:
                    if not (mask & (1 << parent)):  # Parent not selected
                        valid = False
                        break
                if not valid:
                    break
                
                # Add nutritional values and cost
                recipe = recipes[i]
                total_cal += recipe[2][0]
                total_protein += recipe[2][1]
                total_cost += recipe[1]
        
        # If valid and meets requirements
        if valid and total_cal >= min_cal and total_protein >= min_protein:
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != INF else -1