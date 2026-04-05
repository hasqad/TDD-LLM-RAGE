def molecule_to_binary(molecule: str) -> str:
    total = sum(ord(element) for element in molecule)
    return bin(total)