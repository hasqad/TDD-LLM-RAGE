from solution import molecule_to_binary

def test_molecule_to_binary_example():
    assert molecule_to_binary("H2O") == '0b1000110'

def test_molecule_to_binary_large():
    assert molecule_to_binary("C6H12O6") == '0b1110011000011110'

def test_molecule_to_binary_single_element():
    assert molecule_to_binary("H") == '0b65'  # H has ASCII value of 72, but since it's a single element, we only sum once

def test_molecule_to_binary_empty_string():
    assert molecule_to_binary("") == ''