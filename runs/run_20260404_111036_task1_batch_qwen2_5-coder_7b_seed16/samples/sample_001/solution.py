def molecule_to_binary(molecule: str) -> str:
    return '0b' + ''.join(format(ord(element), 'b') for element in molecule)