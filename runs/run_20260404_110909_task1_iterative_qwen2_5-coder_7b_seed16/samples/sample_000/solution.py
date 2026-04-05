def molecule_to_binary(molecule: str) -> str:
    total = 0
    for char in molecule:
        total += ord(char)
    return bin(total)