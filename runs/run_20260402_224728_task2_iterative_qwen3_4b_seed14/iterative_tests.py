from solution import fib

def test_example():
    assert fib(10) == 55

def test_base_case_0():
    assert fib(0) == 0

def test_base_case_1():
    assert fib(1) == 1

def test_small():
    assert fib(5) == 5

def test_larger():
    assert fib(15) == 610
