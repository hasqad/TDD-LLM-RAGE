def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    rows = len(obstacle_grid)
    cols = len(obstacle_grid[0])
    
    if obstacle_grid[0][0] == 1 or obstacle_grid[-1][-1] == 1:
        return 0
        
    dp = [[0] * cols for _ in range(rows)]
    
    dp[0][0] = 1
    
    for j in range(1, cols):
        if obstacle_grid[0][j] == 0:
            dp[0][j] = dp[0][j-1]
        else:
            dp[0][j] = 0
            
    for i in range(1, rows):
        if obstacle_grid[i][0] == 0:
            dp[i][0] = dp[i-1][0]
        else:
            dp[i][0] = 0
            
    for i in range(1, rows):
        for j in range(1, cols):
            if obstacle_grid[i][j] == 0:
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
            else:
                dp[i][j] = 0
                
    return dp[rows-1][cols-1]