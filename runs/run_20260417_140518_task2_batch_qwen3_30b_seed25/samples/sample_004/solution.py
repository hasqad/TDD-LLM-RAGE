def decipher_roman_numeral(roman: str) -> int:
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    n = len(roman)
    for i in range(n - 1):
        if roman_map[roman[i]] < roman_map[roman[i+1]]:
            total -= roman_map[roman[i]]
        else:
            total += roman_map[roman[i]]
    total += roman_map[roman[-1]]
    return total