def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    symbol_values = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    for i in range(len(hieroglyphs)):
        if i > 0 and symbol_values[hieroglyphs[i]] > symbol_values[hieroglyphs[i - 1]]:
            total += symbol_values[hieroglyphs[i]] - 2 * symbol_values[hieroglyphs[i - 1]]
        else:
            total += symbol_values[hieroglyphs[i]]
    return total