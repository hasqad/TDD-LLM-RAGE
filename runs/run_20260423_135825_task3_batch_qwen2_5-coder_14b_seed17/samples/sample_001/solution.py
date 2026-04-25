from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    from functools import lru_cache
    
    @lru_cache(None)
    def dfs(node: int, cal: int, protein: int, cost: int):
        if cal >= min_cal and protein >= min_protein:
            return cost
        min_cost = float('inf')
        for parent in graph[node]:
            min_cost = min(min_cost, dfs(parent, cal, protein, cost))
        name, recipe_cost, (recipe_cal, recipe_protein) = recipes[node]
        if min_cost > dfs(node, cal + recipe_cal, protein + recipe_protein, cost + recipe_cost):
            min_cost = dfs(node, cal + recipe_cal, protein + recipe_protein, cost + recipe_cost)
        return min_cost
    
    result = float('inf')
    for i in range(n):
        if not graph[i]:
            result = min(result, dfs(i, 0, 0, 0))
    
    return result if result != float('inf') else -1