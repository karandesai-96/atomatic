from atomatic import (parse_z_and_symbol,
                      parse_nucleons,
                      parse_relative_atomic_mass,
                      parse_isotopic_composition,
                      parse_std_atomic_weight_and_notes)
from bs4 import BeautifulSoup

test_file = open("test-data/atomatic/test_atomatic.html")
markup = test_file.read()
test_file.close()

test_row = BeautifulSoup(markup, "html.parser").find("tr")
test_row_data = test_row.find_all("td")


def test_parse_z_and_symbol():
    global test_row_data
    obtained_result = dict()

    test_row_data, obtained_result = parse_z_and_symbol(test_row_data,
                                                        obtained_result)
    assert obtained_result["Z"] == 2
    assert obtained_result["Symbol"] == 'He'


def test_parse_nucleons():
    obtained_result = dict()

    obtained_result = parse_nucleons(test_row_data, obtained_result)
    assert obtained_result["Nucleons"] == 3


def test_parse_relative_atomic_mass():
    obtained_result = dict()

    obtained_result = parse_relative_atomic_mass(test_row_data, obtained_result)
    assert obtained_result["Relative Atomic Mass"] == 3.0160293201


def test_parse_isotopic_composition():
    obtained_result = dict()

    obtained_result = parse_isotopic_composition(test_row_data, obtained_result)
    assert obtained_result["Isotopic Composition"] == 0.00000134


def test_parse_std_atomic_weight_and_notes():
    obtained_result = dict()

    obtained_result = parse_std_atomic_weight_and_notes(test_row,
                                                        obtained_result)
    assert obtained_result["Standard Atomic Weight"] == 4.002602
    assert obtained_result["Notes"] == "g,r"
