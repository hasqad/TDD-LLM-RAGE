from collections import deque
from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
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
            new_h = h
            if (new_w, new_h) not in visited:
                visited.add((new_w, new_h))
                queue.append((new_w, new_h, path + ['W']))
        if h > 1:
            new_h = h // 2
            new_w = w
            if (new_w, new_h) not in visited:
                visited.add((new_w, new_h))
                queue.append((new_w, new_h, path + ['H']))
    return []