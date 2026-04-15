from typing import List, Tuple
from collections import deque

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Precompute all possible combinations of recipes and their costs/nutrition
    # Since n <= 20, we can use bitmasking to represent combinations
    INF = float('inf')
    
    # dp[mask] = (min_cost, total_calories, total_protein)
    dp = {}
    dp[0] = (0, 0, 0)
    
    # For each recipe, check if it can be added to existing combinations
    for i in range(n):
        recipe_name, cost, (calories, protein) = recipes[i]
        new_dp = dp.copy()
        
        # Check all existing combinations
        for mask in dp:
            # Check if all dependencies are satisfied
            can_add = True
            for parent in graph[i]:
                if not (mask & (1 << parent)):
                    can_add = False
                    break
            
            if not can_add:
                continue
                
            # Add this recipe to the combination
            new_mask = mask | (1 << i)
            old_cost, old_cal, old_protein = dp[mask]
            new_cost = old_cost + cost
            new_cal = old_cal + calories
            new_protein = old_protein + protein
            
            # Update if this is a better combination
            if new_mask not in new_dp or new_dp[new_mask][0] > new_cost:
                new_dp[new_mask] = (new_cost, new_cal, new_protein)
        
        dp = new_dp
    
    # Find minimum cost among all valid combinations
    min_cost = INF
    for mask in dp:
        cost, cal, protein = dp[mask]
        if cal >= min_cal and protein >= min_protein:
            min_cost = min(min_cost, cost)
    
    return min_cost if min_cost != INF else -1