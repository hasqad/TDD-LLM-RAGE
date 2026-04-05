from solution import is_palindrome

def test_example():
    assert is_palindrome('A man a plan a canal Panama') is True

def test_simple_palindrome():
    assert is_palindrome('racecar') is True

def test_not_palindrome():
    assert is_palindrome('hello') is False

def test_with_punctuation():
    assert is_palindrome('Was it a car or a cat I saw?') is True

def test_single_char():
    assert is_palindrome('a') is True

def test_empty():
    assert is_palindrome('') is True
