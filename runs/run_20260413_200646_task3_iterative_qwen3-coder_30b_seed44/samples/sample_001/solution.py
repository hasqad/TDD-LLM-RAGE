def decode_hieroglyphic_sum(hieroglyphs: str) -> int:
    # Define the values for each hieroglyphic symbol
    values = {'I': 1, 'V': 5, 'X': 10}
    
    total = 0
    i = 0
    
    while i < len(hieroglyphs):
        # Check if we can form a subtractive combination (like IV or IX)
        if i + 1 < len(hieroglyphs):
            # Check for IV (4) or IX (9)
            if hieroglyphs[i] == 'I' and hieroglyphs[i + 1] == 'V':
                total += 4
                i += 2
                continue
            elif hieroglyphs[i] == 'I' and hieroglyphs[i + 1] == 'X':
                total += 9
                i += 2
                continue
        
        # Add the value of the current symbol
        total += values[hieroglyphs[i]]
        i += 1
    
    return total