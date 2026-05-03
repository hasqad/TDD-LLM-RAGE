def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    value_map = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    for i in range(len(hieroglyphs)):
        if i < len(hieroglyphs) - 1 and value_map[hieroglyphs[i]] < value_map[hieroglyphs[i+1]]:
            total -= value_map[hieroglyphs[i]]
        else:
            total += value_map[hieroglyphs[i]]
    return total