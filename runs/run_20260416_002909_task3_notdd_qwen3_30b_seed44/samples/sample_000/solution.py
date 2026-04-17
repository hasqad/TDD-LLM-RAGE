def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    mapping = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    n = len(hieroglyphs)
    for i in range(n):
        if i < n - 1 and mapping[hieroglyphs[i]] < mapping[hieroglyphs[i + 1]]:
            total -= mapping[hieroglyphs[i]]
        else:
            total += mapping[hieroglyphs[i]]
    return total