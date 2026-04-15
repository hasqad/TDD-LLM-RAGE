from typing import List, Tuple
from functools import lru_cache

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Convert graph to a more convenient format
    # graph[i] contains the list of parent recipes for recipe i
    # We need to check if all parents are selected before selecting a recipe
    
    # Precompute all possible combinations of recipes and their costs/nutrition
    # Since n <= 20, we can use bitmasking to represent which recipes are selected
    
    # For each subset of recipes, calculate total cost, calories, and protein
    # But we need to respect the dependency graph
    
    # Use dynamic programming with bitmask
    # dp[mask] = (min_cost, total_calories, total_protein) for recipes in mask
    
    # First, let's validate the dependencies
    # For each recipe, check if all its parents are in the subset
    def is_valid_subset(mask):
        for i in range(n):
            if mask & (1 << i):  # If recipe i is selected
                # Check if all parents are also selected
                for parent in graph[i]:
                    if not (mask & (1 << parent)):
                        return False
        return True
    
    # Precompute for all valid subsets
    min_cost = float('inf')
    
    # Try all possible combinations
    for mask in range(1 << n):
        if not is_valid_subset(mask):
            continue
            
        # Calculate total cost and nutrition for this subset
        total_cost = 0
        total_cal = 0
        total_protein = 0
        
        for i in range(n):
            if mask & (1 << i):
                total_cost += recipes[i][1]
                total_cal += recipes[i][2][0]
                total_protein += recipes[i][2][1]
        
        # Check if this subset meets the requirements
        if total_cal >= min_cal and total_protein >= min_protein:
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != float('inf') else -1