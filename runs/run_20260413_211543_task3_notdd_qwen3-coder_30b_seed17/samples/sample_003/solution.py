from typing import List, Tuple
from collections import deque

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Precompute all possible combinations of recipes and their costs/nutrition
    # Since n <= 20, we can use bitmasking to represent subsets
    # But since dependencies matter, we need to be more careful
    
    # First, let's check if a recipe can be made (all dependencies are satisfied)
    def can_make(recipe_idx, selected):
        for parent in graph[recipe_idx]:
            if parent not in selected:
                return False
        return True
    
    # Try all possible combinations using bitmask
    min_cost = float('inf')
    
    # For each possible subset of recipes
    for mask in range(1 << n):
        selected = set()
        total_cost = 0
        total_cal = 0
        total_protein = 0
        
        # Check if this subset is valid (dependencies satisfied)
        valid = True
        for i in range(n):
            if mask & (1 << i):
                selected.add(i)
                # Check if all dependencies are met
                if not can_make(i, selected):
                    valid = False
                    break
        
        if not valid:
            continue
            
        # Calculate total nutrition and cost
        for i in range(n):
            if mask & (1 << i):
                cost, (cal, protein) = recipes[i][1], recipes[i][2]
                total_cost += cost
                total_cal += cal
                total_protein += protein
        
        # Check if requirements are met
        if total_cal >= min_cal and total_protein >= min_protein:
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != float('inf') else -1