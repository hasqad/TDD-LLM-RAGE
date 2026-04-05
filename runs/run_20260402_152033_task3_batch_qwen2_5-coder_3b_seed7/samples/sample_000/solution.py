from typing import List

def unique_paths_with_obstacles(obstacle_grid: List[List[int]]) -> int:
    if obstacle_grid[0][0] == 1 or obstacle_grid[-1][-1] == 1:
        return 0
    
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    
    # Initialize the DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Start from the top-left corner and fill the DP table
    dp[0][1] = 1
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if obstacle_grid[i - 1][j - 1] == 1:
                continue
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    
    return dp[m][n]