from solution import find_minimal_fold_sequence

def test_seed_8_target_4_4():
    seed = 8
    target_w = 4
    target_h = 4
    result = find_minimal_fold_sequence(seed, target_w, target_h)
    assert result == ["W", "H"]

def test_seed_8_target_8_8():
    seed = 8
    target_w = 8
    target_h = 8
    result = find_minimal_fold_sequence(seed, target_w, target_h)
    assert result == []

def test_seed_8_target_4_8():
    seed = 8
    target_w = 4
    target_h = 8
    result = find_minimal_fold_sequence(seed, target_w, target_h)
    assert result == ["W"]

def test_seed_2_target_1_1():
    seed = 2
    target_w = 1
    target_h = 1
    result = find_minimal_fold_sequence(seed, target_w, target_h)
    assert result == ["W", "H"]

def test_seed_5_target_3_3():
    seed = 5
    target_w = 3
    target_h = 3
    result = find_minimal_fold_sequence(seed, target_w, target_h)
    assert result == []

def test_seed_4_target_1_1():
    seed = 4
    target_w = 1
    target_h = 1
    result = find_minimal_fold_sequence(seed, target_w, target_h)
    assert len(result) == 4
    w, h = seed, seed
    for fold in result:
        if fold == 'W':
            if w > 1:
                w //= 2
        else:
            if h > 1:
                h //= 2
    assert (w, h) == (target_w, target_h)