def decipher_roman_numeral(roman: str) -> int:
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    total = 0
    prev_value = 0
    
    for char in reversed(roman):
        current_value = roman_values[char]
        if current_value >= prev_value:
            total += current_value
        else:
            total -= current_value
        prev_value = current_value
        
    return total