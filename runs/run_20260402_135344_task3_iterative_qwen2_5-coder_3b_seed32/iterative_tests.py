from solution import is_valid

def test_example():
    assert is_valid('()[]{}') is True

def test_nested():
    assert is_valid('({[]})') is True

def test_wrong_order():
    assert is_valid('([)]') is False

def test_unclosed():
    assert is_valid('(') is False

def test_only_closes():
    assert is_valid(')') is False

def test_empty():
    assert is_valid('') is True
