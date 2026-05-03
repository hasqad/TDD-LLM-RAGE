def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    value_map = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    i = 0
    n = len(hieroglyphs)
    while i < n:
        if i + 1 < n and value_map[hieroglyphs[i]] < value_map[hieroglyphs[i+1]]:
            total += value_map[hieroglyphs[i+1]] - value_map[hieroglyphs[i]]
            i += 2
        else:
            total += value_map[hieroglyphs[i]]
            i += 1
    return total