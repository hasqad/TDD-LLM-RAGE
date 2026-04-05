from solution import molecule_to_binary

def test_example():
    assert molecule_to_binary("H2O") == '0b1000110'

def test_empty_molecule():
    assert molecule_to_binary("") == '0b0'

def test_single_element():
    assert molecule_to_binary("C") == '0b67'

def test_multiple_elements():
    assert molecule_to_binary("CO2") == '0b1100111'