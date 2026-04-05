def molecule_to_binary(molecule: str) -> str:
    if not molecule:
        return ''

    element_weights = {
        'H': 72,
        'C': 67,
        'O': 79
    }

    binary_code = ''
    i = 0
    while i < len(molecule):
        letter = molecule[i]
        count = int(molecule[i+1:]) if len(molecule) > i + 1 else 1

        for _ in range(count):
            binary_code += str(element_weights.get(letter, 0))

        i += len(str(count)) + 1

    return bin(int(binary_code))[2:]