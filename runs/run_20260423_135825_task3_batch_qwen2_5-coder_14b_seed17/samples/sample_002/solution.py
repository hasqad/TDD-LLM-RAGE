from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    def dfs(node):
        if memo[node] != -1:
            return memo[node]
        
        cost, calories, protein = recipes[node][1], recipes[node][2][0], recipes[node][2][1]
        
        for parent in graph[node]:
            child_cost = dfs(parent)
            cost += child_cost
            calories += recipes[parent][2][0]
            protein += recipes[parent][2][1]
        
        if calories >= min_cal and protein >= min_protein:
            memo[node] = cost
        else:
            memo[node] = float('inf')
        
        return memo[node]
    
    memo = [-1] * n
    result = float('inf')
    
    for i in range(n):
        if not graph[i]:  # If the recipe has no parents, it's a root node
            result = min(result, dfs(i))
    
    return result if result != float('inf') else -1