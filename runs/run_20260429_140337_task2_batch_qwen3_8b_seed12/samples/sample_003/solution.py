from typing import List
from collections import deque

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    if seed == target_w and seed == target_h:
        return []
    
    queue = deque()
    queue.append((seed, seed, []))
    visited = set()
    visited.add((seed, seed))
    
    while queue:
        current_w, current_h, path = queue.popleft()
        
        if current_w == target_w and current_h == target_h:
            return path
        
        if current_w > 1:
            new_w = current_w // 2
            new_h = current_h
            if (new_w, new_h) not in visited:
                visited.add((new_w, new_h))
                queue.append((new_w, new_h, path + ['W']))
        
        if current_h > 1:
            new_h = current_h // 2
            new_w = current_w
            if (new_w, new_h) not in visited:
                visited.add((new_w, new_h))
                queue.append((new_w, new_h, path + ['H']))
    
    return []