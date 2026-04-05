def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    values = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    i = 0
    n = len(hieroglyphs)
    while i < n:
        if i == n - 1:
            total += values[hieroglyphs[i]]
            break
        if values[hieroglyphs[i]] < values[hieroglyphs[i+1]]:
            total += values[hieroglyphs[i+1]] - values[hieroglyphs[i]]
            i += 2
        else:
            total += values[hieroglyphs[i]]
            i += 1
    return total