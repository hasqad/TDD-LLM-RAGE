def molecule_to_binary(molecule: str) -> str:
    total = sum(ord(char) for char in molecule)
    return bin(total)