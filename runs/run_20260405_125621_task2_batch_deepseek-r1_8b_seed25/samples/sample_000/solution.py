def decipher_roman_numeral(roman: str) -> int:
    mapping = {
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
        if i + 1 < n and mapping[roman[i]] < mapping[roman[i+1]]:
            total += mapping[roman[i+1]] - mapping[roman[i]]
            i += 2
        else:
            total += mapping[roman[i]]
            i += 1
    return total