from solution import unique_paths_with_obstacles

def test_example():
    assert unique_paths_with_obstacles([[0,0,0],[0,1,0],[0,0,0]]) == 2

def test_blocked_start():
    assert unique_paths_with_obstacles([[1,0],[0,0]]) == 0

def test_blocked_end():
    assert unique_paths_with_obstacles([[0,0],[0,1]]) == 0

def test_no_obstacles():
    assert unique_paths_with_obstacles([[0,0,0],[0,0,0]]) == 3

def test_single_row():
    assert unique_paths_with_obstacles([[0,0,1,0]]) == 0

def test_single_cell_free():
    assert unique_paths_with_obstacles([[0]]) == 1
