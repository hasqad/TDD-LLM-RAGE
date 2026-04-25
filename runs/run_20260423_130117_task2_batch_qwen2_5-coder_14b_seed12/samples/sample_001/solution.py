from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    if seed < target_w or seed < target_h:
        return []
    
    folds = []
    current_w, current_h = seed, seed
    
    while current_w > target_w or current_h > target_h:
        if current_w > target_w and current_w % 2 == 0:
            folds.append('W')
            current_w //= 2
        elif current_h > target_h and current_h % 2 == 0:
            folds.append('H')
            current_h //= 2
        else:
            return []
    
    return folds