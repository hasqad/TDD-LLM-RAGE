from solution import decode_hieroglyphic_sum

def test_decode_hieroglyphic_sum_III():
    assert decode_hieroglyphic_sum('III') == 3

def test_decode_hieroglyphic_sum_IX():
    assert decode_hieroglyphic_sum('IX') == 9

def test_decode_hieroglyphic_sum_X():
    assert decode_hieroglyphic_sum('X') == 10

def test_decode_hieroglyphic_sum_IV():
    assert decode_hieroglyphic_sum('IV') == 4