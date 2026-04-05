def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    values = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    prev_value = 0
    for symbol in reversed(hieroglyphs):
        value = values[symbol]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total