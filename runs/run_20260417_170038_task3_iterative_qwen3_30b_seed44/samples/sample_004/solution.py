def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    values = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    n = len(hieroglyphs)
    for i in range(n - 1):
        if values[hieroglyphs[i]] < values[hieroglyphs[i + 1]]:
            total -= values[hieroglyphs[i]]
        else:
            total += values[hieroglyphs[i]]
    total += values[hieroglyphs[-1]]
    return total