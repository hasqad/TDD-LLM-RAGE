def decipher_roman_numeral(roman: str) -> int:
    value_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    i = 0
    while i < len(roman):
        if i + 1 < len(roman) and value_map[roman[i]] < value_map[roman[i+1]]:
            total += value_map[roman[i+1]] - value_map[roman[i]]
            i += 2
        else:
            total += value_map[roman[i]]
            i += 1
    return total