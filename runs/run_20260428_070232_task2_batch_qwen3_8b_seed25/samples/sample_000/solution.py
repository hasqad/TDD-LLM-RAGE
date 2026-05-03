def decipher_roman_numeral(roman: str) -> int:
    roman_values = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
    total = 0
    for i in range(len(roman)):
        current = roman_values[roman[i]]
        if i < len(roman)-1 and current < roman_values[roman[i+1]]:
            total -= current
        else:
            total += current
    return total