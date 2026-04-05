def decipher_roman_numeral(roman: str) -> int:
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    i = 0
    n = len(roman)
    while i < n:
        if i + 1 < n and roman_values[roman[i]] < roman_values[roman[i+1]]:
            total += roman_values[roman[i+1]] - roman_values[roman[i]]
            i += 2
        else:
            total += roman_values[roman[i]]
            i += 1
    return total