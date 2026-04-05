def decipher_roman_numeral(roman: str) -> int:
    roman_map = {
        'M': 1000,
        'D': 500,
        'C': 100,
        'L': 50,
        'X': 10,
        'V': 5,
        'I': 1
    }
    total = 0
    i = 0
    while i < len(roman):
        if i < len(roman) - 1 and roman_map[roman[i]] < roman_map[roman[i+1]]:
            total += roman_map[roman[i+1]] - roman_map[roman[i]]
            i += 2
        else:
            total += roman_map[roman[i]]
            i += 1
    return total