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
            j = i + 2
            while j < len(molecule) and molecule[j].isdigit():
                count *= 10
                try:
                    count += int(molecule[j])
                except ValueError:
                    break
                j += 1
            if element in atomic_weights:
                binary_code += bin(atomic_weights[element])[2:] * (count - 1)
            else:
                raise ValueError(f"Invalid molecule: {molecule}")
        elif molecule[i].isalpha():
            count = 1
            element = molecule[i]
            i += 1

            while i < len(molecule) and molecule[i].isdigit():
                count *= 10
                try:
                    count += int(molecule[i])
                except ValueError:
                    break
                i += 1

            if element in atomic_weights:
                binary_code += bin(atomic_weights[element])[2:] * (count - 1)

        i += 1

    return '0b' + binary_code if binary_code else ''