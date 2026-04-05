from solution import decode_hieroglyphic_sum

def test_decode_hieroglyphic_sum():
    assert decode_hieroglyphic_sum('III') == 3

def test_decode_hieroglyphic_sum_IX():
    assert decode_hieroglyphic_sum('IX') == 9

def test_decode_hieroglyphic_sum_LVIII():
    assert decode_hieroglyphic_sum('LVIII') == 58

def test_decode_hieroglyphic_sum_single_I():
    assert decode_hieroglyphic_sum('I') == 1

def test_decode_hieroglyphic_sum_single_V():
    assert decode_hieroglyphic_sum('V') == 5

def test_decode_hieroglyphic_sum_single_X():
    assert decode_hieroglyphic_sum('X') == 10