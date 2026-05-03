def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    value = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    for i in range(len(hieroglyphs)):
        current = value[hieroglyphs[i]]
        if i < len(hieroglyphs) - 1:
            next_val = value[hieroglyphs[i+1]]
            if current < next_val:
                total -= current
            else:
                total += current
        else:
            total += current
    return total