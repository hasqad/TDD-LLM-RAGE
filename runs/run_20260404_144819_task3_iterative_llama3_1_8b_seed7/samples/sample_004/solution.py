def unique_paths_with_obstacles(obstacle_grid):
    m = len(obstacle_grid)
    n = len(obstacle_grid[0])
    
    if obstacle_grid[0][0] == 1 or obstacle_grid[m-1][n-1] == 1:
        return 0
    
    directions = [(0, 1), (1, 0)]
    queue = [(0, 0, 1)]
    visited = {(0, 0)}
    
    while queue:
        x, y, count = queue.pop(0)
        
        if x == m - 1 and y == n - 1:
            return count
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if (nx < m and ny < n) and obstacle_grid[nx][ny] == 0 and (nx, ny) not in visited:
                queue.append((nx, ny, count + 1))
                visited.add((nx, ny))

    return 0