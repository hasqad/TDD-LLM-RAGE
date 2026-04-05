def minimal_folds(start, target):
    if start == target:
        return 0
    current = start
    folds = 0
    while current != target and current > 1:
        current = current // 2
        folds += 1
    if current == target:
        return folds
    else:
        return None

def find_minimal_fold_sequence(seed, target_w, target_h):
    w_folds = minimal_folds(seed, target_w)
    h_folds = minimal_folds(seed, target_h)
    if w_folds is None or h_folds is None:
        return []
    return ['W'] * w_folds + ['H'] * h_folds