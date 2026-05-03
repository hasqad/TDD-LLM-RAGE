from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    def is_achievable(target):
        if seed % target != 0:
            return False
        ratio = seed // target
        return (ratio & (ratio - 1)) == 0
    
    if not (is_achievable(target_w) and is_achievable(target_h)):
        return []
    
    def count_folds(ratio):
        count = 0
        while ratio % 2 == 0:
            ratio //= 2
            count += 1
        return count
    
    w_ratio = seed // target_w
    w_folds = count_folds(w_ratio)
    h_ratio = seed // target_h
    h_folds = count_folds(h_ratio)
    
    return ['W'] * w_folds + ['H'] * h_folds