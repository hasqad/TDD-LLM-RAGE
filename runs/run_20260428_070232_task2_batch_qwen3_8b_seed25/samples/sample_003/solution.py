def decipher_roman_numeral(roman: str) -> int:
    values = {'I':1, 'V':5, 'X':10, 'L':50, 'C':100, 'D':500, 'M':1000}
    total = 0
    for i in range(len(roman)):
        current_val = values[roman[i]]
        if i < len(roman) - 1:
            next_val = values[roman[i+1]]
            if current_val < next_val:
                total -= current_val
            else:
                total += current_val
        else:
            total += current_val
    return total