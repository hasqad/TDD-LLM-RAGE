def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    mapping = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    i = 0
    n = len(hieroglyphs)
    while i < n:
        if i < n - 1 and mapping[hieroglyphs[i]] < mapping[hieroglyphs[i+1]]:
            total += mapping[hieroglyphs[i+1]] - mapping[hieroglyphs[i]]
            i += 2
        else:
            total += mapping[hieroglyphs[i]]
            i += 1
    return total