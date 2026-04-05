def molecule_to_binary(molecule: str) -> str:
    atomic_weights = {
        'H': 1,
        'C': 12,
        'O': 16,
        # Add more elements as needed...
    }
    
    binary_code = ''
    i = 0
    while i < len(molecule):
        if molecule[i].isdigit():
            count = int(molecule[i])
            element = molecule[i + 1]
            i += 2
            if element in atomic_weights:
                ascii_sum = ord(element) * count
                binary_code += bin(ascii_sum)[2:]
            else:
                return "Invalid molecule"
        else:
            element = molecule[i]
            i += 1
            if element in atomic_weights:
                ascii_sum = ord(element)
                binary_code += bin(ascii_sum)[2:]
            else:
                return "Invalid molecule"

    return '0b' + binary_code