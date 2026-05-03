from solution import decipher_roman_numeral

def test_decipher_roman_numeral():
    assert decipher_roman_numeral('XXIII') == 23
    assert decipher_roman_numeral('IV') == 4
    assert decipher_roman_numeral('MCMXCIV') == 1994
    assert decipher_roman_numeral('I') == 1
    assert decipher_roman_numeral('III') == 3