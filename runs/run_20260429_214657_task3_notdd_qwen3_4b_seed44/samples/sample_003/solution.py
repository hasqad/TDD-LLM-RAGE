def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    value_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50}
    total = 0
    i = 0
    n = len(hieroglyphs)
    while i < n:
        if i + 1 < n:
            if hieroglyphs[i] == 'I' and hieroglyphs[i+1] == 'V':
                total += 4
                i += 2
            elif hieroglyphs[i] == 'I' and hieroglyphs[i+1] == 'X':
                total += 9
                i += 2
            elif hieroglyphs[i] == 'X' and hieroglyphs[i+1] == 'L':
                total += 40
                i += 2
            else:
                total += value_map[hieroglyphs[i]]
                i += 1
        else:
            total += value_map[hieroglyphs[i]]
            i += 1
    return total