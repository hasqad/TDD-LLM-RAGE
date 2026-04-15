from typing import List, Tuple
from collections import deque

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Precompute all possible combinations of recipes and their costs/nutrition
    # Use bitmask to represent which recipes are selected
    min_cost = float('inf')
    
    # For each possible combination of recipes (represented as bitmask)
    for mask in range(1 << n):
        # Check if all dependencies are satisfied
        valid = True
        total_cal = 0
        total_protein = 0
        total_cost = 0
        
        for i in range(n):
            if mask & (1 << i):  # If recipe i is selected
                # Check if all dependencies are also selected
                for parent in graph[i]:
                    if not (mask & (1 << parent)):
                        valid = False
                        break
                if not valid:
                    break
                
                # Add recipe's nutrition and cost
                recipe = recipes[i]
                total_cal += recipe[2][0]
                total_protein += recipe[2][1]
                total_cost += recipe[1]
        
        # If combination is valid and meets requirements
        if valid and total_cal >= min_cal and total_protein >= min_protein:
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != float('inf') else -1