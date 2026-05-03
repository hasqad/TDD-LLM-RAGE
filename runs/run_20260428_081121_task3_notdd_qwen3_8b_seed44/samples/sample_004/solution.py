def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    values = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    for i in range(len(hieroglyphs)):
        current = hieroglyphs[i]
        current_val = values[current]
        if i < len(hieroglyphs) - 1:
            next_val = values[hieroglyphs[i+1]]
            if current_val < next_val:
                total -= current_val
            else:
                total += current_val
        else:
            total += current_val
    return total