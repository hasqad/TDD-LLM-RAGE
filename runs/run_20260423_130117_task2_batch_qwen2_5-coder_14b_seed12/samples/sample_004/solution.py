from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    if target_w > seed or target_h > seed:
        return []
    
    sequence = []
    current_w, current_h = seed, seed
    
    while current_w > target_w or current_h > target_h:
        if current_w > target_w and current_w % 2 == 0:
            sequence.append('W')
            current_w //= 2
        elif current_h > target_h and current_h % 2 == 0:
            sequence.append('H')
            current_h //= 2
        else:
            return []
    
    return sequence