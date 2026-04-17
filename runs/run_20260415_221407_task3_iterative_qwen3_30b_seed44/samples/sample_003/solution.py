def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    roman_map = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    n = len(hieroglyphs)
    for i in range(n):
        current_val = roman_map[hieroglyphs[i]]
        if i < n - 1 and current_val < roman_map[hieroglyphs[i+1]]:
            total -= current_val
        else:
            total += current_val
    return total