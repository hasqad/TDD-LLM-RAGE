from collections import deque
from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    if target_w > seed or target_h > seed:
        return []
    
    if seed == target_w and seed == target_h:
        return []
    
    queue = deque()
    queue.append((seed, seed, []))
    visited = set()
    visited.add((seed, seed))
    
    while queue:
        w, h, path = queue.popleft()
        if w == target_w and h == target_h:
            return path
            
        if w > 1:
            new_w = w // 2
            new_state = (new_w, h)
            if new_state not in visited:
                new_path = path + ['W']
                queue.append((new_w, h, new_path))
                visited.add(new_state)
                
        if h > 1:
            new_h = h // 2
            new_state = (w, new_h)
            if new_state not in visited:
                new_path = path + ['H']
                queue.append((w, new_h, new_path))
                visited.add(new_state)
                
    return []