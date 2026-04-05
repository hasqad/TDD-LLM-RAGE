def molecule_to_binary(molecule: str) -> str:
    weights = {'H': 1, 'C': 12, 'O': 16}
    binary_code = ''
    for char in molecule:
        if char.isalpha():
            element = char
            count = int(''.join(filter(str.isdigit, molecule[molecule.index(char):])))
            if count == 0 or (count > 1 and char != 'H'):
                raise ValueError("Invalid chemical formula")
            binary_code += bin(sum(ord(element) + weights[element] * count))[2:]
    return '0b' + binary_code