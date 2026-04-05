def molecule_to_binary(molecule: str) -> str:
    if not molecule:
        return ''

    elements = {}
    for char in molecule:
        if char.isalpha():
            element = char
            count = 1
            while molecule[molecule.index(char) + 1].isdigit():
                count *= int(molecule[molecule.index(char) + 1])
                molecule = molecule[:molecule.index(char) + 1] + molecule[molecule.index(char) + 2:]
            if element in elements:
                elements[element] += count
            else:
                elements[element] = count

    binary_code = ''
    for element, count in elements.items():
        binary_code += bin(ord(element))[2:] * count

    return '0b' + binary_code