def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    values = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    for i in range(len(hieroglyphs)):
        if i + 1 < len(hieroglyphs) and values[hieroglyphs[i]] < values[hieroglyphs[i + 1]]:
            total -= values[hieroglyphs[i]]
        else:
            total += values[hieroglyphs[i]]
    return total