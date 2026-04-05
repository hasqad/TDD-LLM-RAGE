def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    total = 0
    i = 0
    n = len(hieroglyphs)
    while i < n:
        if i + 1 < n and hieroglyphs[i:i+2] in ['IV', 'IX']:
            if hieroglyphs[i:i+2] == 'IV':
                total += 4
            else:
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