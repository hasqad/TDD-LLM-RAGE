def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> list[str]:
    if target_w == seed and target_h == seed:
        return []
    
    # If target dimensions are larger than seed, it's impossible
    if target_w > seed or target_h > seed:
        return []
    
    # If either target dimension is 1, we need to fold down to 1
    # We can only fold if the current dimension is > 1
    
    # Greedy approach: try to reduce each dimension as much as possible
    w, h = seed, seed
    sequence = []
    
    # While we haven't reached the target dimensions
    while w > target_w or h > target_h:
        # If we can't reduce either dimension further, it's impossible
        if w <= 1 and h <= 1:
            return []
        
        # If we can reduce width and it's not already at target
        if w > 1 and w > target_w:
            w //= 2
            sequence.append("W")
        # If we can reduce height and it's not already at target
        elif h > 1 and h > target_h:
            h //= 2
            sequence.append("H")
        # If we can reduce width but it's already at target, try height
        elif w > 1 and w <= target_w and h > 1 and h > target_h:
            h //= 2
            sequence.append("H")
        # If we can reduce height but it's already at target, try width
        elif h > 1 and h <= target_h and w > 1 and w > target_w:
            w //= 2
            sequence.append("W")
        else:
            # If we can't make progress, it's impossible
            return []
    
    # Verify the sequence works
    w, h = seed, seed
    for fold in sequence:
        if fold == "W":
            if w > 1:
                w //= 2
        else:  # fold == "H"
            if h > 1:
                h //= 2
    
    if w == target_w and h == target_h:
        return sequence
    else:
        # Try a different approach - BFS to find shortest path
        from collections import deque
        
        queue = deque([(seed, seed, [])])
        visited = set()
        visited.add((seed, seed))
        
        while queue:
            curr_w, curr_h, path = queue.popleft()
            
            if curr_w == target_w and curr_h == target_h:
                return path
            
            # Try folding width
            if curr_w > 1:
                new_w = curr_w // 2
                if (new_w, curr_h) not in visited:
                    visited.add((new_w, curr_h))
                    queue.append((new_w, curr_h, path + ["W"]))
            
            # Try folding height
            if curr_h > 1:
                new_h = curr_h // 2
                if (curr_w, new_h) not in visited:
                    visited.add((curr_w, new_h))
                    queue.append((curr_w, new_h, path + ["H"]))
        
        return []