from solution import spiral_order

def test_3x3():
    assert spiral_order([[1,2,3],[4,5,6],[7,8,9]]) == [1,2,3,6,9,8,7,4,5]

def test_single_row():
    assert spiral_order([[1,2,3,4]]) == [1,2,3,4]

def test_single_col():
    assert spiral_order([[1],[2],[3]]) == [1,2,3]

def test_single_element():
    assert spiral_order([[42]]) == [42]

def test_2x2():
    assert spiral_order([[1,2],[3,4]]) == [1,2,4,3]

def test_3x4():
    assert spiral_order([[1,2,3,4],[5,6,7,8],[9,10,11,12]]) == [1,2,3,4,8,12,11,10,9,5,6,7]
