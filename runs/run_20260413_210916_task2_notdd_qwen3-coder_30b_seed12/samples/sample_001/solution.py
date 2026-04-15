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
    
    queue = deque([(seed, seed, [])])  # (current_width, current_height, sequence)
    visited = set()
    visited.add((seed, seed))
    
    while queue:
        width, height, sequence = queue.popleft()
        
        # Try folding width
        if width > 1:
            new_width = width // 2
            new_height = height
            new_sequence = sequence + ['W']
            
            if new_width == target_w and new_height == target_h:
                return new_sequence
            
            if (new_width, new_height) not in visited:
                visited.add((new_width, new_height))
                queue.append((new_width, new_height, new_sequence))
        
        # Try folding height
        if height > 1:
            new_width = width
            new_height = height // 2
            new_sequence = sequence + ['H']
            
            if new_width == target_w and new_height == target_h:
                return new_sequence
            
            if (new_width, new_height) not in visited:
                visited.add((new_width, new_height))
                queue.append((new_width, new_height, new_sequence))
    
    return []