def molecule_to_binary(molecule: str) -> str:
    element_weights = {
        'H': 1,
        'C': 12,
        'O': 16
    }
    binary_code = ''
    i = 0
    while i < len(molecule):
        if molecule[i].isdigit():
            count = int(molecule[i])
            element = molecule[i + 1]
            weight_sum = (count * ord(element)) + (ord(element) - 64)
            binary_code += format(weight_sum, 'b')
            i += 2
        else:
            element = molecule[i]
            weight_sum = ord(element) - 64
            binary_code += format(weight_sum, 'b')
            i += 1
    return '0b' + binary_code