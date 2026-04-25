from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    def dfs(recipe_index: int, memo: dict) -> int:
        if (recipe_index, min_cal, min_protein) in memo:
            return memo[(recipe_index, min_cal, min_protein)]
        
        name, cost, (calories, protein) = recipes[recipe_index]
        
        # If the current recipe meets or exceeds the minimum requirements
        if calories >= min_cal and protein >= min_protein:
            return cost
        
        # Calculate the cost of including this recipe
        include_cost = float('inf')
        for parent in graph[recipe_index]:
            include_cost = min(include_cost, dfs(parent, memo))
        
        # If we can't meet the requirements with parents, return infinity
        if include_cost == float('inf'):
            return float('inf')
        
        # Total cost including this recipe
        total_cost = include_cost + cost
        
        # Check if this total cost meets the minimum requirements
        if calories + sum(recipes[parent][2][0] for parent in graph[recipe_index]) >= min_cal and \
           protein + sum(recipes[parent][2][1] for parent in graph[recipe_index]) >= min_protein:
            memo[(recipe_index, min_cal, min_protein)] = total_cost
        else:
            memo[(recipe_index, min_cal, min_protein)] = float('inf')
        
        return memo[(recipe_index, min_cal, min_protein)]
    
    # Start DFS from each recipe and find the minimum cost
    min_total_cost = float('inf')
    for i in range(n):
        min_total_cost = min(min_total_cost, dfs(i, {}))
    
    return min_total_cost if min_total_cost != float('inf') else -1

# Example usage:
# print(recipe_chain_optimization(3, [("Recipe1", 10, (5, 5)), ("Recipe2", 20, (10, 10)), ("Recipe3", 30, (15, 15))], [[], [0], [0]], 20, 10))