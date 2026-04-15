from typing import List, Tuple
from collections import deque

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Precompute all possible combinations of recipes and their costs/nutrition
    # Use bitmask to represent which recipes are selected
    min_cost = float('inf')
    
    # Check all possible combinations of recipes (2^n combinations)
    for mask in range(1 << n):
        # Check if all dependencies are satisfied
        valid = True
        selected_recipes = []
        
        for i in range(n):
            if mask & (1 << i):
                selected_recipes.append(i)
                # Check if all parents are selected
                for parent in graph[i]:
                    if not (mask & (1 << parent)):
                        valid = False
                        break
                if not valid:
                    break
        
        if not valid:
            continue
            
        # Calculate total cost and nutrition
        total_cost = 0
        total_cal = 0
        total_protein = 0
        
        for i in selected_recipes:
            total_cost += recipes[i][1]
            total_cal += recipes[i][2][0]
            total_protein += recipes[i][2][1]
        
        # Check if minimum requirements are met
        if total_cal >= min_cal and total_protein >= min_protein:
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != float('inf') else -1