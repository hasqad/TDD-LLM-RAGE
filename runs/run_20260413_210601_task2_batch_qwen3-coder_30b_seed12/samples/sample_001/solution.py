from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    if target_w == seed and target_h == seed:
        return []
    
    # If target dimensions are larger than seed, it's impossible
    if target_w > seed or target_h > seed:
        return []
    
    # If either target dimension is 1, we need to check if it's reachable
    # by folding from the seed dimension
    if target_w == 1 and target_h == 1:
        # We need to fold both dimensions to 1
        # This is only possible if seed is a power of 2
        w, h = seed, seed
        sequence = []
        while w > 1 or h > 1:
            if w > 1 and h > 1:
                # Choose the dimension that gets us closer to 1
                if w > h:
                    w //= 2
                    sequence.append('W')
                else:
                    h //= 2
                    sequence.append('H')
            elif w > 1:
                w //= 2
                sequence.append('W')
            elif h > 1:
                h //= 2
                sequence.append('H')
        # Check if we reached the target
        if w == 1 and h == 1:
            return sequence
        else:
            return []
    
    # For other cases, we use a greedy approach
    w, h = seed, seed
    sequence = []
    
    # We need to find a sequence of folds that reduces w to target_w and h to target_h
    # This is essentially finding a path in a binary tree where each node represents
    # a possible dimension, and we want to reach (target_w, target_h)
    
    # Try to build the sequence greedily
    while w > target_w or h > target_h:
        # If we can't fold further in either dimension, return empty list
        if w == 1 and h == 1:
            return []
        
        # If we can fold width
        if w > target_w and w > 1:
            w //= 2
            sequence.append('W')
        # If we can fold height
        elif h > target_h and h > 1:
            h //= 2
            sequence.append('H')
        # If we can't fold either dimension but haven't reached target
        else:
            # Check if we're stuck
            if w > target_w or h > target_h:
                # This means we can't reach the target
                return []
    
    # Verify that we reached the target
    if w == target_w and h == target_h:
        return sequence
    else:
        return []