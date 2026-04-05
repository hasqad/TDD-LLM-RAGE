def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    dp = [[0]*n for _ in range(m)]
    
    if obstacle_grid[0][0] == 1 or obstacle_grid[m-1][n-1] == 1:
        return 0
    
    dp[0][0] = 1
    for i in range(1, m):
        if obstacle_grid[i][0] != 1 and dp[i-1][0] != 0:
            dp[i][0] = dp[i-1][0]
    
    for j in range(1, n):
        if obstacle_grid[0][j] != 1 and dp[0][j-1] != 0:
            dp[0][j] = dp[0][j-1]
    
    for i in range(1, m):
        for j in range(1, n):
            if obstacle_grid[i][j] == 1:
                continue
            elif i == m-1 and j == n-1:
                return dp[i][j]
            else:
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
    
    return dp[m-1][n-1]