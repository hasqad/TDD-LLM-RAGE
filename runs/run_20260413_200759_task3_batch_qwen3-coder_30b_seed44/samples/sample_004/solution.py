def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    # Define the values for each hieroglyph
    values = {'I': 1, 'V': 5, 'X': 10}
    
    total = 0
    prev_value = 0
    
    # Process each character from right to left
    for char in reversed(hieroglyphs):
        current_value = values[char]
        # If current value is less than previous, subtract it (for cases like IV, IX)
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value
        prev_value = current_value
    
    return total