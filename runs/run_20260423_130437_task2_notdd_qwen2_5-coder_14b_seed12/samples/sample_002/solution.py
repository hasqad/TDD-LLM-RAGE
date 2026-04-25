from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    if target_w > seed or target_h > seed:
        return []
    
    sequence = []
    current_w, current_h = seed, seed
    
    while current_w != target_w:
        if current_w % 2 == 0 and current_w // 2 >= target_w:
            current_w //= 2
            sequence.append('W')
        else:
            break
    
    while current_h != target_h:
        if current_h % 2 == 0 and current_h // 2 >= target_h:
            current_h //= 2
            sequence.append('H')
        else:
            break
    
    if current_w == target_w and current_h == target_h:
        return sequence
    else:
        return []