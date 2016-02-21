from utils import soup_utils as su
from utils import text_utils as tu
import os
import pandas as pd


def fetch_atomic_dataset():
    url = "http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"

    if os.path.isfile("outdump/mainsoup.html"):
        physics_nist_soup = su.get_soup_from_file("mainsoup.html")
    else:
        physics_nist_soup = su.get_soup_from_url(url)
        su.store_content_from_soup(physics_nist_soup, filename="mainsoup.html")

    headings = ["Z", "Symbol", "Nucleons", "Relative Atomic Mass", "Isotopic \
                Composition", "Standard Atomic Weight", "Notes"]

    atomic_dataset = pd.DataFrame(columns=headings)

    rows = physics_nist_soup.find_all("tr")
    for _ in range(4, 15):
        df_record = fetch_row(rows[_])
        if df_record is not None:
            print df_record
    return


def fetch_row(row):
    df_record = dict()

    row_data = row.find_all("td")

    # ignoring the row containing blue line and other stray rows
    if len(row_data) < 3 or row_data[0].has_attr("colspan"):
        return None

    row_data, df_record = parse_z_and_symbol(row_data, df_record)
    df_record = parse_nucleons(row_data, df_record)
    df_record = parse_isotopic_composition(row_data, df_record)

    # standard atomic weight and additional notes are only present in record
    # of first isotope of any element
    if row_data[0] is not None:
        df_record = parse_std_atomic_weight_and_notes(row, df_record)
    return df_record


def parse_z_and_symbol(row_data, df_record):

    if row_data[0].get("valign") == "top":
        # this happens when the record is a new element - Z will be followed by
        # symbol of the element
        df_record["Z"] = int(tu.unicode_to_utf8(row_data[0].text))
        df_record["Symbol"] = tu.unicode_to_utf8(row_data[1].text)
    else:
        # this means current record is an isotope of previous record,
        # Z and symbol entries in record will be missing (except H, D, T)
        df_record["Z"] = None
        df_record["Symbol"] = None
        # dummy entries in row_data : Z at index 0 and symbol at index 1
        row_data.insert(0, None)
        row_data.insert(1, None)

    # this condition is only for H, D, T records in the whole table
    # D, T will be third entry in list due to dummy entries added in else block
    if row_data[2].get("align") == "center":
        df_record["Symbol"] = tu.unicode_to_utf8(row_data[2].text)
        row_data.pop(1)

    return row_data, df_record


def parse_nucleons(row_data, df_record):
    # third entry in record will be number of nucleons (stored as integer)
    # no checks required as this entry exists in all valid records
    df_record["Nucleons"] = int(tu.unicode_to_utf8(row_data[2].text))

    return df_record


def parse_relative_atomic_mass(row_data, df_record):
    # fourth entry in record will be relative atomic mass of that isotope
    relative_atomic_mass = tu.parse_float(row_data[3].text)
    df_record["Relative Atomic Mass"] = relative_atomic_mass

    return df_record


def parse_isotopic_composition(row_data, df_record):
    # fifth entry in record will be isotopic composition of that isotope
    # try-except block is needed as this entry might be absent
    try:
        isotopic_composition = tu.parse_float(row_data[4].text)
        df_record["Isotopic Composition"] = isotopic_composition
    except ValueError:
        df_record["Isotopic Composition"] = None

    return df_record


def parse_std_atomic_weight_and_notes(row, df_record):
    std_atomic_weight = row.find_next_sibling("td")

    if std_atomic_weight is not None:
        text = tu.parse_float_list(std_atomic_weight.text)
        df_record["Standard Atomic Weight"] = text

        notes = std_atomic_weight.find_next_sibling("td")

        if std_atomic_weight is not None:
            text = tu.unicode_to_utf8(notes.text)
            df_record["Notes"] = text
        else:
            df_record["Notes"] = None
    else:
        df_record["Standard Atomic Weight"] = None

    return df_record


if __name__ == "__main__":
    fetch_atomic_dataset()
