def decipher_roman_numeral(roman: str) -> int:
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    prev_val = 0
    for char in roman[::-1]:
        current_val = roman_map[char]
        if current_val < prev_val:
            total -= current_val
        else:
            total += current_val
        prev_val = current_val
    return total