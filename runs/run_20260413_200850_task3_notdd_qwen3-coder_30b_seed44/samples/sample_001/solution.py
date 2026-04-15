def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    # Define the values for each hieroglyphic symbol
    values = {'I': 1, 'V': 5, 'X': 10}
    
    total = 0
    i = 0
    
    while i < len(hieroglyphs):
        # If we're not at the last character and current value is less than next value,
        # we have a subtractive case (like IV or IX)
        if i < len(hieroglyphs) - 1 and values[hieroglyphs[i]] < values[hieroglyphs[i + 1]]:
            total += values[hieroglyphs[i + 1]] - values[hieroglyphs[i]]
            i += 2  # Skip both characters
        else:
            total += values[hieroglyphs[i]]
            i += 1  # Move to next character
    
    return total