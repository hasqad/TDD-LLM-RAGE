def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> list[str]:
    if target_w == seed and target_h == seed:
        return []
    
    # If target dimensions are larger than seed, it's impossible
    if target_w > seed or target_h > seed:
        return []
    
    # If either target dimension is 1, we need to fold to that dimension
    # We'll use a greedy approach: fold the dimension that's further from target
    w, h = seed, seed
    sequence = []
    
    # While we haven't reached the target dimensions
    while w > target_w or h > target_h:
        # If we can't fold further in either dimension, return empty list
        if w == 1 and h == 1:
            return []
        
        # If we can't fold width anymore, fold height
        if w <= target_w:
            if h > target_h and h > 1:
                h //= 2
                sequence.append("H")
            else:
                return []
        # If we can't fold height anymore, fold width
        elif h <= target_h:
            if w > target_w and w > 1:
                w //= 2
                sequence.append("W")
            else:
                return []
        # Otherwise, fold the dimension that's further from target
        else:
            if w > h:
                w //= 2
                sequence.append("W")
            else:
                h //= 2
                sequence.append("H")
    
    # Verify that we've reached the target
    if w == target_w and h == target_h:
        return sequence
    else:
        return []