def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    if not obstacle_grid or not obstacle_grid[0]:
        return 0
    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    if obstacle_grid[0][0] == 1 or obstacle_grid[-1][-1] == 1:
        return 0
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for j in range(1, n):
        if obstacle_grid[0][j] == 0:
            dp[0][j] = dp[0][j-1]
        else:
            dp[0][j] = 0
    for i in range(1, m):
        if obstacle_grid[i][0] == 0:
            dp[i][0] = dp[i-1][0]
        else:
            dp[i][0] = 0
    for i in range(1, m):
        for j in range(1, n):
            if obstacle_grid[i][j] == 1:
                dp[i][j] = 0
            else:
                dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[-1][-1]