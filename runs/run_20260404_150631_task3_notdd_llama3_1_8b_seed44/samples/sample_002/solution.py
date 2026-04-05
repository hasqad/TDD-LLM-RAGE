def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    roman_values = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    for i in range(len(hieroglyphs)):
        if i > 0 and roman_values[hieroglyphs[i]] > roman_values[hieroglyphs[i - 1]]:
            total += roman_values[hieroglyphs[i]] - 2 * roman_values[hieroglyphs[i - 1]]
        else:
            total += roman_values[hieroglyphs[i]]
    return total