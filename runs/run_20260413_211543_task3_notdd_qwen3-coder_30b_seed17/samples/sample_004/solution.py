from typing import List, Tuple
from collections import deque

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    # Convert graph to adjacency list for easier processing
    # We need to process recipes in topological order
    in_degree = [0] * n
    for i in range(n):
        for parent in graph[i]:
            in_degree[parent] += 1
    
    # Topological sort using Kahn's algorithm
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    # Process in topological order
    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for parent in graph[node]:
            in_degree[parent] -= 1
            if in_degree[parent] == 0:
                queue.append(parent)
    
    # For each subset of recipes, calculate the minimum cost to achieve required nutrition
    # Since n <= 20, we can use bitmasks
    min_cost = float('inf')
    
    # For each possible combination of recipes (bitmask)
    for mask in range(1 << n):
        # Check if all dependencies are satisfied
        valid = True
        total_cal = 0
        total_protein = 0
        total_cost = 0
        
        for i in range(n):
            if mask & (1 << i):
                # Check if all parents are selected
                for parent in graph[i]:
                    if not (mask & (1 << parent)):
                        valid = False
                        break
                if not valid:
                    break
                
                # Add recipe values
                recipe = recipes[i]
                total_cal += recipe[2][0]
                total_protein += recipe[2][1]
                total_cost += recipe[1]
        
        # If valid combination and meets requirements
        if valid and total_cal >= min_cal and total_protein >= min_protein:
            min_cost = min(min_cost, total_cost)
    
    return min_cost if min_cost != float('inf') else -1