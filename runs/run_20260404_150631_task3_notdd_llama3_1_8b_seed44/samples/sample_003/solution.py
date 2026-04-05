def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    hieroglyph_values = {'I': 1, 'V': 5, 'X': 10}
    total_sum = 0
    for i in range(len(hieroglyphs)):
        if i > 0 and hieroglyph_values[hieroglyphs[i]] > hieroglyph_values[hieroglyphs[i - 1]]:
            total_sum += hieroglyph_values[hieroglyphs[i]] - 2 * hieroglyph_values[hieroglyphs[i - 1]]
        else:
            total_sum += hieroglyph_values[hieroglyphs[i]]
    return total_sum