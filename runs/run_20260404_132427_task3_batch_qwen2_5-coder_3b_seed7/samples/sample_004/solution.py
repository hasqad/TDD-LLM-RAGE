from typing import List

def unique_paths_with_obstacles(obstacle_grid: List[List[int]]) -> int:
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    
    # If start or end is blocked, return 0
    if obstacle_grid[0][0] == 1 or obstacle_grid[m-1][n-1] == 1:
        return 0
    
    # Initialize the DP table with zeros
    dp = [[0] * n for _ in range(m)]
    
    # Set the starting point to 1
    dp[0][0] = 1
    
    # Fill the first row and first column of the DP table
    for i in range(1, m):
        if obstacle_grid[i][0] == 0:
            dp[i][0] = dp[i-1][0]
    for j in range(1, n):
        if obstacle_grid[0][j] == 0:
            dp[0][j] = dp[0][j-1]
    
    # Fill the rest of the DP table
    for i in range(1, m):
        for j in range(1, n):
            if obstacle_grid[i][j] == 0:
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    # The bottom-right corner of the DP table contains the answer
    return dp[m-1][n-1]