def decipher_roman_numeral(roman: str) -> int:
    roman_to_value = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
    total = 0
    for i in range(len(roman) - 1):
        current = roman[i]
        next_char = roman[i+1]
        if roman_to_value[current] < roman_to_value[next_char]:
            total -= roman_to_value[current]
        else:
            total += roman_to_value[current]
    total += roman_to_value[roman[-1]]
    return total