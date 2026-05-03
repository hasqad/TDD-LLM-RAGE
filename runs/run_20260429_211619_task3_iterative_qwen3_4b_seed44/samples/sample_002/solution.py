def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    roman_map = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    i = 0
    n = len(hieroglyphs)
    while i < n:
        if i < n - 1 and roman_map[hieroglyphs[i]] < roman_map[hieroglyphs[i+1]]:
            total += roman_map[hieroglyphs[i+1]] - roman_map[hieroglyphs[i]]
            i += 2
        else:
            total += roman_map[hieroglyphs[i]]
            i += 1
    return total