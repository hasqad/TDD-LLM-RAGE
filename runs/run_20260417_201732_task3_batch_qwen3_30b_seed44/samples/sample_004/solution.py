def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    roman_map = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    n = len(hieroglyphs)
    for i in range(n - 1):
        if roman_map[hieroglyphs[i]] < roman_map[hieroglyphs[i+1]]:
            total -= roman_map[hieroglyphs[i]]
        else:
            total += roman_map[hieroglyphs[i]]
    total += roman_map[hieroglyphs[-1]]
    return total