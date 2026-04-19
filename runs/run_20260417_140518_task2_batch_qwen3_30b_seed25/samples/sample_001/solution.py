def decipher_roman_numeral(roman: str) -> int:
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    n = len(roman)
    for i in range(n - 1):
        if roman_values[roman[i]] < roman_values[roman[i+1]]:
            total -= roman_values[roman[i]]
        else:
            total += roman_values[roman[i]]
    total += roman_values[roman[-1]]
    return total