from typing import List, Tuple
from collections import deque

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Precompute all possible combinations of recipes and their costs/nutrition
    # Since n <= 20, we can use bitmasking to represent combinations
    INF = float('inf')
    
    # Convert graph to adjacency list for easier processing
    adj_list = [set(parents) for parents in graph]
    
    # Check if a recipe can be selected (all parents are selected)
    def can_select(recipe_idx, selected_mask):
        parents = set(graph[recipe_idx])
        for parent in parents:
            if not (selected_mask & (1 << parent)):
                return False
        return True
    
    # Try all possible combinations using bitmask
    min_cost = INF
    
    # For each possible combination of recipes
    for mask in range(1 << n):
        # Check if all dependencies are satisfied
        valid = True
        for i in range(n):
            if mask & (1 << i):  # If recipe i is selected
                if not can_select(i, mask):
                    valid = False
                    break
        
        if not valid:
            continue
            
        # Calculate total cost and nutrition for this combination
        total_cost = 0
        total_cal = 0
        total_protein = 0
        
        for i in range(n):
            if mask & (1 << i):
                cost, (cal, protein) = recipes[i][1], recipes[i][2]
                total_cost += cost
                total_cal += cal
                total_protein += protein
        
        # Check if this combination meets the requirements
        if total_cal >= min_cal and total_protein >= min_protein:
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != INF else -1