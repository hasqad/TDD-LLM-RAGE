from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    # Check if target is reachable
    if target_w > seed or target_h > seed:
        return []
    
    # If already at target, no folds needed
    if target_w == seed and target_h == seed:
        return []
    
    # Work backwards from target to seed
    w, h = target_w, target_h
    sequence = []
    
    # While we haven't reached the original dimensions
    while w < seed or h < seed:
        # If width is less than seed, we can fold it
        if w < seed:
            # If width is even, we can fold it in half
            if seed % 2 == 0:
                seed //= 2
                sequence.append('W')
            else:
                # If seed is odd, we can't fold it in half
                return []
        # If height is less than seed, we can fold it
        elif h < seed:
            # If height is even, we can fold it in half
            if seed % 2 == 0:
                seed //= 2
                sequence.append('H')
            else:
                # If seed is odd, we can't fold it in half
                return []
    
    # This approach is flawed. Let's restart with a better approach.
    
    # Start with current dimensions
    current_w, current_h = seed, seed
    sequence = []
    
    # While we haven't reached target dimensions
    while current_w > target_w or current_h > target_h:
        # Try to reduce width first
        if current_w > target_w:
            # Check if we can halve width
            if current_w % 2 == 0:
                current_w //= 2
                sequence.append('W')
            else:
                # If width is odd and we need to reduce it, it's impossible
                # unless we're already at target
                return []
        
        # Try to reduce height
        elif current_h > target_h:
            # Check if we can halve height
            if current_h % 2 == 0:
                current_h //= 2
                sequence.append('H')
            else:
                # If height is odd and we need to reduce it, it's impossible
                return []
    
    # Reverse the sequence to get the correct order
    return sequence[::-1]