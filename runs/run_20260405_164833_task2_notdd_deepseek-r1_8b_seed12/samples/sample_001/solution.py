from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    if target_w > seed or target_h > seed:
        return []
    
    k_w = 0
    temp = seed
    while temp != target_w:
        if temp <= target_w:
            break
        temp = temp // 2
        k_w += 1
    
    if temp != target_w:
        return []
    
    k_h = 0
    temp = seed
    while temp != target_h:
        if temp <= target_h:
            break
        temp = temp // 2
        k_h += 1
    
    if temp != target_h:
        return []
    
    return ['W'] * k_w + ['H'] * k_h