import os
from bs4 import BeautifulSoup
from atomatic import (parse_z_and_symbol,
                      parse_nucleons,
                      parse_relative_atomic_mass,
                      parse_isotopic_composition,
                      parse_std_atomic_weight_and_notes,
                      fetch_row, fetch_atomic_dataset)
import pandas as pd


test_file = open(os.path.join(os.curdir, "bin/test-data/test_atomatic.html"))
markup = test_file.read()
test_file.close()

test_row = BeautifulSoup(markup, "html.parser").find("tr")
test_row_data = test_row.find_all("td")

expected_atomic_dataset = pd.read_csv(os.path.join(os.curdir,
                                           "bin/test-data/expected_result.csv"))


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
    assert obtained_result["Standard Atomic Weight"] == "4.002602"
    assert obtained_result["Notes"] == "g,r"


def test_fetch_row():
    obtained_result = fetch_row(test_row)
    assert obtained_result["Z"] == 2
    assert obtained_result["Symbol"] == 'He'
    assert obtained_result["Nucleons"] == 3
    assert obtained_result["Relative Atomic Mass"] == 3.0160293201
    assert obtained_result["Isotopic Composition"] == 0.00000134
    assert obtained_result["Standard Atomic Weight"] == "4.002602"
    assert obtained_result["Notes"] == "g,r"


def test_fetch_atomic_dataset():

    # first time to ensure the soup is generated from request response content
    # and mainsoup.html gets generated
    if os.path.isfile(os.path.join(os.curdir, "bin/mainsoup.html")):
        os.remove(os.path.join(os.curdir, "bin/mainsoup.html"))
    obtained_atomic_dataset = fetch_atomic_dataset()

    # getting alternate rows just to save time, as all assertions need to be
    # done just once, even rows here, odd rows next
    for _ in range(0, len(obtained_atomic_dataset), 2):
        assert obtained_atomic_dataset.get(_) == expected_atomic_dataset.get(_)

    # second time to ensure the soup is generated from mainsoup.html
    # to simply increase code coverage
    obtained_atomic_dataset = fetch_atomic_dataset()

    for _ in range(1, len(obtained_atomic_dataset), 2):
        assert obtained_atomic_dataset.get(_) == expected_atomic_dataset.get(_)
