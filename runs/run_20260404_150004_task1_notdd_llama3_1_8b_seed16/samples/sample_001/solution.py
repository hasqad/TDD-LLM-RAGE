def molecule_to_binary(molecule: str) -> str:
    element_weights = {
        'H': 1,
        'C': 12,
        'O': 16,
        # Add more elements as needed...
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
        
        ascii_sum = ord(element) * multiplier + (element in element_weights and element_weights[element] or 0)
        binary_code += bin(ascii_sum)[2:]
    
    return '0b' + binary_code