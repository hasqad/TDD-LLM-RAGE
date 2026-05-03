def decipher_roman_numeral(roman: str) -> int:
    roman_to_value = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
    total = 0
    for i in range(len(roman) - 1):
        current = roman_to_value[roman[i]]
        next_val = roman_to_value[roman[i+1]]
        if current < next_val:
            total -= current
        else:
            total += current
    total += roman_to_value[roman[-1]]
    return total