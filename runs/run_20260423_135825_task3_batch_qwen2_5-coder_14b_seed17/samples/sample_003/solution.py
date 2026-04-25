from typing import List, Tuple

def recipe_chain_optimization(n: int, recipes: List[Tuple[str, int, Tuple[int, int]]], graph: List[List[int]], min_cal: int, min_protein: int) -> int:
    def dfs(node: int, dp: List[int]) -> int:
        if dp[node] != -1:
            return dp[node]
        
        # Calculate the cost and nutritional values for the current recipe
        name, cost, (calories, protein) = recipes[node]
        total_cost = cost
        total_calories = calories
        total_protein = protein
        
        # Add the costs and nutritional values of all dependent recipes
        for parent in graph[node]:
            parent_cost = dfs(parent, dp)
            total_cost += parent_cost
            total_calories += recipes[parent][2][0]
            total_protein += recipes[parent][2][1]
        
        # Check if the current combination meets the minimum requirements
        if total_calories >= min_cal and total_protein >= min_protein:
            dp[node] = total_cost
        else:
            dp[node] = float('inf')
        
        return dp[node]
    
    # Initialize DP array with -1
    dp = [-1] * n
    
    # Calculate the minimum cost for each recipe starting from 0 to n-1
    min_total_cost = float('inf')
    for i in range(n):
        if not graph[i]:  # Only start from recipes with no parents
            min_total_cost = min(min_total_cost, dfs(i, dp))
    
    return min_total_cost if min_total_cost != float('inf') else -1