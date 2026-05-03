from collections import deque
from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    if seed == target_w and seed == target_h:
        return []
    
    visited = set()
    queue = deque()
    queue.append((seed, seed, []))
    visited.add((seed, seed))
    
    while queue:
        current_w, current_h, path = queue.popleft()
        
        if current_w == target_w and current_h == target_h:
            return path
        
        # Try 'W' fold
        if current_w > 1 and current_w % 2 == 0:
            new_w = current_w // 2
            new_h = current_h
            if (new_w, new_h) not in visited:
                visited.add((new_w, new_h))
                queue.append((new_w, new_h, path + ['W']))
        
        # Try 'H' fold
        if current_h > 1 and current_h % 2 == 0:
            new_h = current_h // 2
            new_w = current_w
            if (new_w, new_h) not in visited:
                visited.add((new_w, new_h))
                queue.append((new_w, new_h, path + ['H']))
    
    return []