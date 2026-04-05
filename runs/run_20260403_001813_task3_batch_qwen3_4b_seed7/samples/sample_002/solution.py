def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    dp = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if obstacle_grid[i][j] == 1:
                dp[i][j] = 0
            else:
                if i == 0 and j == 0:
                    dp[i][j] = 1
                else:
                    top = dp[i-1][j] if i > 0 else 0
                    left = dp[i][j-1] if j > 0 else 0
                    dp[i][j] = top + left
    return dp[m-1][n-1]