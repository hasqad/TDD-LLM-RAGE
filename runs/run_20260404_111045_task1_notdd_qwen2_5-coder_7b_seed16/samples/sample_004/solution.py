def molecule_to_binary(molecule: str) -> str:
    total_ascii = sum(ord(char) for char in molecule)
    return bin(total_ascii)