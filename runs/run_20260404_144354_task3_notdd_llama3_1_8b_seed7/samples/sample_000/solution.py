def unique_paths_with_obstacles(obstacle_grid):
    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    
    if obstacle_grid[0][0] == 1 or obstacle_grid[m-1][n-1] == 1:
        return 0
    
    obstacle_grid[0][0] = 1
    for i in range(1, m):
        if obstacle_grid[i][0] != 1:
            obstacle_grid[i][0] = obstacle_grid[i-1][0]
    
    for j in range(1, n):
        if obstacle_grid[0][j] != 1:
            obstacle_grid[0][j] = obstacle_grid[0][j-1]
            
    for i in range(1, m):
        for j in range(1, n):
            if obstacle_grid[i][j] != 1:
                obstacle_grid[i][j] = obstacle_grid[i-1][j] + obstacle_grid[i][j-1]
    
    return obstacle_grid[m-1][n-1]