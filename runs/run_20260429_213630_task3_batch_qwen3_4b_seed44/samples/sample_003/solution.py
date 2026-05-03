def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    symbol_map = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    i = 0
    n = len(hieroglyphs)
    while i < n:
        if i + 1 < n and symbol_map[hieroglyphs[i]] < symbol_map[hieroglyphs[i+1]]:
            total += symbol_map[hieroglyphs[i+1]] - symbol_map[hieroglyphs[i]]
            i += 2
        else:
            total += symbol_map[hieroglyphs[i]]
            i += 1
    return total