from solution import decode_hieroglyphic_sum

def test_decode_hieroglyphic_sum_example():
    assert decode_hieroglyphic_sum('III') == 3
    assert decode_hieroglyphic_sum('IX') == 9
    assert decode_hieroglyphic_sum('LVIII') == 58

def test_decode_hieroglyphic_sum_single_symbol():
    assert decode_hieroglyphic_sum('I') == 1
    assert decode_hieroglyphic_sum('V') == 5
    assert decode_hieroglyphic_sum('X') == 10

def test_decode_hieroglyphic_sum_large_number():
    assert decode_hieroglyphic_sum('MCMXCIV') == 1994