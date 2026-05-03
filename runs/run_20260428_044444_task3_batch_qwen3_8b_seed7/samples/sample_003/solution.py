def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    
    if obstacle_grid[0][0] == 1 or obstacle_grid[m-1][n-1] == 1:
        return 0
    
    for i in range(m):
        for j in range(n):
            if obstacle_grid[i][j] == 1:
                obstacle_grid[i][j] = 0
            else:
                if i == 0 and j == 0:
                    obstacle_grid[i][j] = 1
                else:
                    if i == 0:
                        obstacle_grid[i][j] = obstacle_grid[i][j-1]
                    elif j == 0:
                        obstacle_grid[i][j] = obstacle_grid[i-1][j]
                    else:
                        obstacle_grid[i][j] = obstacle_grid[i-1][j] + obstacle_grid[i][j-1]
    
    return obstacle_grid[m-1][n-1]