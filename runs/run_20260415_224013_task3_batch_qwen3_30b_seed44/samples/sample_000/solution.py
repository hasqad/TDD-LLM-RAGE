def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    values = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    n = len(hieroglyphs)
    for i in range(n):
        if i < n - 1 and values[hieroglyphs[i]] < values[hieroglyphs[i+1]]:
            total -= values[hieroglyphs[i]]
        else:
            total += values[hieroglyphs[i]]
    return total