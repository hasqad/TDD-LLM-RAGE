from functools import lru_cache

def unique_paths_with_obstacles(obstacle_grid: list[list[int]]) -> int:
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    
    @lru_cache(None)
    def dp(x, y):
        if x == m or y == n or obstacle_grid[x][y] == 1:
            return 0
        if x == m - 1 and y == n - 1:
            return 1
        
        return dp(x + 1, y) + dp(x, y + 1)
    
    return dp(0, 0)