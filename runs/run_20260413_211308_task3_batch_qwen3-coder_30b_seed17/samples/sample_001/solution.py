from typing import List, Tuple
from functools import lru_cache

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Precompute all possible combinations of recipes and their costs/nutrition
    @lru_cache(maxsize=None)
    def dfs(node, cal, protein, visited):
        # If we've met the requirements, return 0 cost
        if cal >= min_cal and protein >= min_protein:
            return 0
        
        # If we've visited all nodes, return infinity
        if len(visited) == n:
            return float('inf')
        
        # Get all children that can be visited (dependencies satisfied)
        min_cost = float('inf')
        
        # Try all unvisited recipes
        for i in range(n):
            if i not in visited:
                # Check if all dependencies are satisfied
                can_visit = True
                for dep in graph[i]:
                    if dep not in visited:
                        can_visit = False
                        break
                
                if can_visit:
                    # Add this recipe
                    recipe_name, cost, (cals, prot) = recipes[i]
                    new_cal = cal + cals
                    new_protein = protein + prot
                    new_visited = visited | {i}
                    
                    result = dfs(i, new_cal, new_protein, new_visited)
                    if result != float('inf'):
                        min_cost = min(min_cost, cost + result)
        
        return min_cost
    
    # Try starting from each recipe
    min_total_cost = float('inf')
    
    # For each recipe, try starting with it
    for i in range(n):
        # Check if this recipe can be started (no dependencies)
        if len(graph[i]) == 0:
            recipe_name, cost, (cals, prot) = recipes[i]
            # Start with this recipe
            result = dfs(i, cals, prot, {i})
            if result != float('inf'):
                min_total_cost = min(min_total_cost, cost + result)
    
    # Also consider combinations of recipes
    # Use bitmasks to try all combinations
    min_cost = float('inf')
    
    # Try all subsets of recipes
    for mask in range(1 << n):
        # Check if this subset is valid (dependencies satisfied)
        valid = True
        total_cal = 0
        total_protein = 0
        total_cost = 0
        
        for i in range(n):
            if mask & (1 << i):
                # Check dependencies
                for dep in graph[i]:
                    if not (mask & (1 << dep)):
                        valid = False
                        break
                if not valid:
                    break
                # Add recipe values
                _, cost, (cals, prot) = recipes[i]
                total_cal += cals
                total_protein += prot
                total_cost += cost
        
        if valid and total_cal >= min_cal and total_protein >= min_protein:
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != float('inf') else -1