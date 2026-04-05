from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    # Check for width
    current_w = seed
    k1 = 0
    while current_w >= target_w:
        if current_w == target_w:
            break
        current_w //= 2
        k1 += 1
    else:
        return []
    
    # Check for height
    current_h = seed
    k2 = 0
    while current_h >= target_h:
        if current_h == target_h:
            break
        current_h //= 2
        k2 += 1
    else:
        return []
    
    return ['W'] * k1 + ['H'] * k2