from typing import List, Tuple
from collections import deque

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Precompute dependencies for each recipe
    def get_dependencies(recipe_idx):
        deps = set()
        queue = deque([recipe_idx])
        while queue:
            current = queue.popleft()
            for parent in graph[current]:
                if parent not in deps:
                    deps.add(parent)
                    queue.append(parent)
        return deps
    
    # Generate all possible combinations of recipes
    # Since n <= 20, we can use bitmasking
    min_cost = float('inf')
    
    # For each possible combination of recipes
    for mask in range(1 << n):
        # Check if this combination satisfies dependencies
        valid = True
        selected_recipes = []
        
        for i in range(n):
            if mask & (1 << i):
                selected_recipes.append(i)
                # Check if all dependencies are satisfied
                for dep in graph[i]:
                    if not (mask & (1 << dep)):
                        valid = False
                        break
                if not valid:
                    break
        
        if not valid:
            continue
            
        # Calculate total calories, protein and cost
        total_cal = 0
        total_protein = 0
        total_cost = 0
        
        for recipe_idx in selected_recipes:
            cost, (cal, protein) = recipes[recipe_idx][1], recipes[recipe_idx][2]
            total_cal += cal
            total_protein += protein
            total_cost += cost
            
        # Check if minimum requirements are met
        if total_cal >= min_cal and total_protein >= min_protein:
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != float('inf') else -1