from solution import min_distance

def test_example():
    assert min_distance('horse', 'ros') == 3

def test_intention_execution():
    assert min_distance('intention', 'execution') == 5

def test_empty_to_word():
    assert min_distance('', 'abc') == 3

def test_word_to_empty():
    assert min_distance('abc', '') == 3

def test_same_word():
    assert min_distance('abc', 'abc') == 0

def test_single_chars():
    assert min_distance('a', 'b') == 1
