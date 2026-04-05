def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    mapping = {'I': 1, 'V': 5, 'X': 10}
    i = 0
    total = 0
    n = len(hieroglyphs)
    while i < n:
        if i + 1 < n and hieroglyphs[i] == 'I' and hieroglyphs[i+1] in ['V', 'X']:
            total += mapping[hieroglyphs[i+1]] - mapping[hieroglyphs[i]]
            i += 2
        else:
            total += mapping[hieroglyphs[i]]
            i += 1
    return total