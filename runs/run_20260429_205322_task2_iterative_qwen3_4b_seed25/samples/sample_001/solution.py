def decipher_roman_numeral(roman: str) -> int:
    roman_map = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    total = 0
    i = 0
    n = len(roman)
    while i < n:
        if i == n - 1:
            total += roman_map[roman[i]]
            break
        if roman_map[roman[i]] < roman_map[roman[i+1]]:
            total += roman_map[roman[i+1]] - roman_map[roman[i]]
            i += 2
        else:
            total += roman_map[roman[i]]
            i += 1
    return total