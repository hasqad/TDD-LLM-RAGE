def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> list[str]:
    if target_w == seed and target_h == seed:
        return []
    
    # If target dimensions are larger than seed, it's impossible
    if target_w > seed or target_h > seed:
        return []
    
    # If either target dimension is 1, we need to fold it down
    # We'll use a greedy approach: fold the dimension that's further from target
    w, h = seed, seed
    sequence = []
    
    # While we haven't reached the target dimensions
    while w > target_w or h > target_h:
        # If we can't fold further in either dimension, return empty list
        if w == 1 and h == 1:
            return []
        
        # If width is greater than target, fold it
        if w > target_w and w > 1:
            w //= 2
            sequence.append("W")
        # If height is greater than target, fold it
        elif h > target_h and h > 1:
            h //= 2
            sequence.append("H")
        # If we can't fold either dimension further but haven't reached target
        else:
            # Check if we're stuck because of odd numbers
            # This is a special case - we might need to backtrack or find another approach
            # Let's try a more systematic approach
            break
    
    # Verify if we reached the target
    if w == target_w and h == target_h:
        return sequence
    
    # If we're still not at target, we need to be more systematic
    # Let's try a BFS approach to find the minimal path
    
    from collections import deque
    
    # BFS to find minimal sequence
    queue = deque([(seed, seed, [])])  # (width, height, sequence)
    visited = set()
    visited.add((seed, seed))
    
    while queue:
        curr_w, curr_h, seq = queue.popleft()
        
        if curr_w == target_w and curr_h == target_h:
            return seq
            
        # Try folding width
        if curr_w > 1:
            new_w = curr_w // 2
            new_h = curr_h
            if (new_w, new_h) not in visited:
                visited.add((new_w, new_h))
                queue.append((new_w, new_h, seq + ["W"]))
        
        # Try folding height
        if curr_h > 1:
            new_w = curr_w
            new_h = curr_h // 2
            if (new_w, new_h) not in visited:
                visited.add((new_w, new_h))
                queue.append((new_w, new_h, seq + ["H"]))
    
    return []