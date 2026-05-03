def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    value_map = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    for i in range(len(hieroglyphs) - 1):
        current = value_map[hieroglyphs[i]]
        next_val = value_map[hieroglyphs[i+1]]
        if current < next_val:
            total -= current
        else:
            total += current
    total += value_map[hieroglyphs[-1]]
    return total