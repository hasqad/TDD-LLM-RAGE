def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    if obstacle_grid[0][0] == 1 or obstacle_grid[-1][-1] == 1:
        return 0
    
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    
    # Initialize the DP table with zeros
    dp = [[0 for _ in range(n)] for _ in range(m)]
    
    # Start point has one path
    dp[0][0] = 1
    
    # Fill the first row and first column
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
    
    return dp[-1][-1]