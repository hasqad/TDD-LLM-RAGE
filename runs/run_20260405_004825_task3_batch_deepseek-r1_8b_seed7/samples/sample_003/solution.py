def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    if not obstacle_grid or not obstacle_grid[0]:
        return 0
    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    if obstacle_grid[0][0] == 1 or obstacle_grid[m-1][n-1] == 1:
        return 0
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            if obstacle_grid[i][j] == 1:
                dp[i][j] = 0
            else:
                top = dp[i-1][j] if i-1 >= 0 else 0
                left = dp[i][j-1] if j-1 >= 0 else 0
                dp[i][j] = top + left
    return dp[m-1][n-1]