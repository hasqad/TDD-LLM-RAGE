def decipher_roman_numeral(roman: str) -> int:
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    for i in range(len(roman)):
        if i > 0 and roman_numerals[roman[i]] > roman_numerals[roman[i - 1]]:
            result += roman_numerals[roman[i]] - 2 * roman_numerals[roman[i - 1]]
        else:
            result += roman_numerals[roman[i]]
    return result