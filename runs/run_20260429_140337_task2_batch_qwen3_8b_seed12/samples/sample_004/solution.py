from typing import List

def find_minimal_fold_sequence(seed: int, target_w: int, target_h: int) -> List[str]:
    def is_reachable(seed, target):
        if target > seed:
            return False
        if seed % target != 0:
            return False
        quotient = seed // target
        return (quotient & (quotient - 1)) == 0

    if not (is_reachable(seed, target_w) and is_reachable(seed, target_h)):
        return []

    steps_w = 0
    current_w = seed
    while current_w > target_w:
        current_w = current_w // 2
        steps_w += 1

    steps_h = 0
    current_h = seed
    while current_h > target_h:
        current_h = current_h // 2
        steps_h += 1

    return ['W'] * steps_w + ['H'] * steps_h