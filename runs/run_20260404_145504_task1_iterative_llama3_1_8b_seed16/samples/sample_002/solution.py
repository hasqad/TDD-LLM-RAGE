def molecule_to_binary(molecule: str) -> str:
    atomic_weights = {
        'H': 1,
        'C': 12,
        'O': 16
    }
    binary_code = ''
    i = 0
    while i < len(molecule):
        if molecule[i].isdigit():
            multiplier = int(molecule[i])
            element = molecule[i+1]
            i += 2
        else:
            multiplier = 1
            element = molecule[i]
            i += 1
        symbol_sum = ord(element) + atomic_weights.get(element, 0) * multiplier
        binary_code += bin(symbol_sum)[2:]
    return '0b' + binary_code if binary_code else ''