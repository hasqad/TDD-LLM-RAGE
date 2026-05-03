from typing import List
from collections import deque

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    if target_w > seed or target_h > seed:
        return []
    if target_w == seed and target_h == seed:
        return []
    queue = deque()
    visited = set()
    queue.append((seed, seed, []))
    visited.add((seed, seed))
    while queue:
        current_w, current_h, path = queue.popleft()
        if current_w == target_w and current_h == target_h:
            return path
        if current_w > 1:
            new_w = current_w // 2
            new_h = current_h
            new_state = (new_w, new_h)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_w, new_h, path + ['W']))
        if current_h > 1:
            new_h = current_h // 2
            new_w = current_w
            new_state = (new_w, new_h)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_w, new_h, path + ['H']))
    return []