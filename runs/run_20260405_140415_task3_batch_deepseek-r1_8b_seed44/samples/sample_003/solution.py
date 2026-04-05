def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    total = 0
    i = 0
    n = len(hieroglyphs)
    while i < n:
        if i + 1 < n and hieroglyphs[i] == 'I' and hieroglyphs[i+1] == 'V':
            total += 4
            i += 2
        elif i + 1 < n and hieroglyphs[i] == 'I' and hieroglyphs[i+1] == 'X':
            total += 9
            i += 2
        else:
            if hieroglyphs[i] == 'I':
                total += 1
            elif hieroglyphs[i] == 'V':
                total += 5
            elif hieroglyphs[i] == 'X':
                total += 10
            i += 1
    return total