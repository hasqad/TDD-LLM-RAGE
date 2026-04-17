def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    value_map = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    n = len(hieroglyphs)
    for i in range(n - 1):
        if value_map[hieroglyphs[i]] < value_map[hieroglyphs[i+1]]:
            total -= value_map[hieroglyphs[i]]
        else:
            total += value_map[hieroglyphs[i]]
    total += value_map[hieroglyphs[-1]]
    return total