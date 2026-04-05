def molecule_to_binary(molecule: str) -> str:
    atomic_weights = {
        'H': 1,
        'C': 12,
        'O': 16
    }
    
    binary_code = ''
    for char in molecule:
        if char.isalpha():
            weight = atomic_weights.get(char, 0)
            binary_code += bin(ord(char))[2:]
            if not char.isdigit():
                binary_code += bin(weight)[2:]
        else:
            count = int(char)
            last_char = molecule[molecule.index(char) - 1]
            weight = atomic_weights[last_char]
            for _ in range(count):
                binary_code += bin(weight)[2:]

    return '0b' + binary_code