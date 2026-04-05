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
            element = molecule[i+1]
            while i + 1 < len(molecule) and molecule[i+1].isdigit():
                count *= 10
                try:
                    count += int(molecule[i+1])
                except ValueError:
                    break
                i += 1
            if element in atomic_weights:
                binary_code += bin(atomic_weights[element] * count)[2:]
            else:
                raise ValueError(f"Invalid molecule: {molecule}")
        else:
            try:
                atomic_weights[molecule[i]]
            except KeyError:
                raise ValueError(f"Invalid molecule: {molecule}")
            binary_code += bin(atomic_weights[molecule[i]])[2:]
        i += 1

    return '0b' + binary_code