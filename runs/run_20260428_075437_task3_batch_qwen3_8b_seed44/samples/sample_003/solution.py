def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    values = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    for i in range(len(hieroglyphs)):
        current = values[hieroglyphs[i]]
        if i < len(hieroglyphs) - 1 and current < values[hieroglyphs[i + 1]]:
            total -= current
        else:
            total += current
    return total