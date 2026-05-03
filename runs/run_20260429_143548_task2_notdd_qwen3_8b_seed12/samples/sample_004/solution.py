from typing import List
from collections import deque

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    if target_w > seed or target_h > seed:
        return []
    
    def is_achievable(dim, seed_dim):
        if dim == 0:
            return False
        if seed_dim % dim != 0:
            return False
        ratio = seed_dim // dim
        return (ratio & (ratio - 1)) == 0
    
    if not (is_achievable(target_w, seed) and is_achievable(target_h, seed)):
        return []
    
    visited = set()
    queue = deque()
    queue.append((seed, seed, []))
    visited.add((seed, seed))
    
    while queue:
        current_w, current_h, path = queue.popleft()
        if current_w == target_w and current_h == target_h:
            return path
        # Try fold W
        if current_w > 1:
            new_w = current_w // 2
            new_h = current_h
            state = (new_w, new_h)
            if state not in visited:
                visited.add(state)
                queue.append((new_w, new_h, path + ['W']))
        # Try fold H
        if current_h > 1:
            new_h = current_h // 2
            new_w = current_w
            state = (new_w, new_h)
            if state not in visited:
                visited.add(state)
                queue.append((new_w, new_h, path + ['H']))
    
    return []