from typing import List
from collections import deque

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    def is_power_of_two(n):
        return n > 0 and (n & (n - 1)) == 0
    
    if seed % target_w != 0 or not is_power_of_two(seed // target_w):
        return []
    if seed % target_h != 0 or not is_power_of_two(seed // target_h):
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
            new_path = path + ['W']
            if (new_w, new_h) not in visited:
                visited.add((new_w, new_h))
                queue.append((new_w, new_h, new_path))
        if current_h > 1:
            new_h = current_h // 2
            new_w = current_w
            new_path = path + ['H']
            if (new_w, new_h) not in visited:
                visited.add((new_w, new_h))
                queue.append((new_w, new_h, new_path))
    return []