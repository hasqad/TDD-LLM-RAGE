from solution import num_decodings

def test_example():
    # "226" -> "BZ"(2,26), "VF"(22,6), "BBF"(2,2,6) -> 3 ways
    assert num_decodings("226") == 3

def test_single_zero():
    assert num_decodings("0") == 0

def test_leading_zero():
    assert num_decodings("06") == 0

def test_ten():
    # "10" -> "J"(10) only -> 1 way
    assert num_decodings("10") == 1

def test_single_digit():
    assert num_decodings("7") == 1

def test_complex():
    # "11106" -> "AAJF"(1,1,10,6), "KJF"(11,10,6) -> 2 ways
    assert num_decodings("11106") == 2
