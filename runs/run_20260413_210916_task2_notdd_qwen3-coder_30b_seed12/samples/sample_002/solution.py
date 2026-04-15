from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    # Check if target dimensions are valid
    if target_w > seed or target_h > seed or target_w <= 0 or target_h <= 0:
        return []
    
    # If already at target dimensions
    if target_w == seed and target_h == seed:
        return []
    
    # BFS to find shortest sequence
    from collections import deque
    
    queue = deque([(seed, seed, [])])  # (width, height, sequence)
    visited = set()
    visited.add((seed, seed))
    
    while queue:
        width, height, sequence = queue.popleft()
        
        # If we reached the target
        if width == target_w and height == target_h:
            return sequence
        
        # Try folding width
        if width > 1:
            new_width = width // 2
            new_state = (new_width, height)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_width, height, sequence + ['W']))
        
        # Try folding height
        if height > 1:
            new_height = height // 2
            new_state = (width, new_height)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((width, new_height, sequence + ['H']))
    
    # If we get here, target is unreachable
    return []