from atomatic import parse_z_and_symbol
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
