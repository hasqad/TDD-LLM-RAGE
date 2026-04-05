def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    value = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    i = 0
    n = len(hieroglyphs)
    while i < n:
        if hieroglyphs[i] == 'I' and i + 1 < n and hieroglyphs[i+1] in ['V', 'X']:
            total += value[hieroglyphs[i+1]] - value[hieroglyphs[i]]
            i += 2
        else:
            total += value[hieroglyphs[i]]
            i += 1
    return total