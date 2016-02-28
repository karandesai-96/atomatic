from utils import soup_utils as su
from utils import text_utils as tu
from utils import db_utils as dbu
import os
import pandas as pd


def fetch_atomic_dataset():
    """
    * Fetches the atomic dataset available at mentioned url in html tabular
      format and parses it into a pandas DataFrame.
    * It uses methods from soup_utils.py and forms a BeautifulSoup using request
      response content of url.
    * It iteratively goes through each row (`<tr>` tag) and makes calls to
      helper function, `fetch_row` written below to parse the data and
      categorize it properly.

    :return: data_frame: pandas DataFrame containing the parsed atomic dataset
    """

    url = "http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"

    # writes request response content to a file and uses it subsequently,
    # done for speeding up and avoiding multiple requests while debugging
    if os.path.isfile(os.path.join(os.curdir, "bin/mainsoup.html")):
        soup = su.get_soup_from_file("mainsoup.html")
    else:
        soup = su.get_soup_from_url(url)
        su.store_content_from_soup(soup, filename="mainsoup.html")

    # each will form a column of data frame
    headings = ["Z", "Symbol", "Nucleons", "Relative Atomic Mass",
                "Isotopic Composition", "Standard Atomic Weight", "Notes"]

    data_frame = pd.DataFrame(columns=headings)

    # iterate through each row of the table and obtain a dictionary having
    # keys same as those mentioned in headings list
    for row in soup.find_all("tr"):
        df_record = fetch_row(row)
        if df_record is not None:
            data_frame = data_frame.append(df_record, ignore_index=True)

    return data_frame


def fetch_row(row):
    """
    Fetches the data by parsing a single row. Collection is done by making
    various calls to methods listed below which parse single entry of the row
    and add appropriate key value pair in the dictionary.

    :param row: BeautifulSoup tag for a row in table. Contains `<td>` tags
                having the needed data.
    :return: df_record: a record for single isotope of any element to be
                appended at the end of the data frame. If row doesn't have
                required data (blue line, or stray) then NoneType is returned.
    """
    df_record = dict()

    row_data = row.find_all("td")

    # ignore the row containing blue line and other stray rows
    if len(row_data) < 3 or row_data[0].has_attr("colspan"):
        return None

    # parse and add all the entries of the record one by one
    row_data, df_record = parse_z_and_symbol(row_data, df_record)
    df_record = parse_nucleons(row_data, df_record)
    df_record = parse_relative_atomic_mass(row_data, df_record)
    df_record = parse_isotopic_composition(row_data, df_record)

    # standard atomic weight and additional notes are only present in record
    # of first isotope of any element
    if row_data[0] is not None:
        df_record = parse_std_atomic_weight_and_notes(row, df_record)
    return df_record


def parse_z_and_symbol(row_data, df_record):
    """
    * Parses the atomic number Z and the symbol of element. It adds two keys in
      the dictionary passed as parameter - 'Z' and 'Symbol'. If these entries do
      not exist in a record (incase of subsequent isotopes of one element), then
      they are set to None.
    * Dummy members in the row_data list are appended at start if these entries
      do not exist, to generalize indexing.

    :param row_data: list of `<td>` tags in a single row.
    :param df_record: existing dictionary containing already parsed entries.
    :return: Modified list (after appending dummy members added if any) and
    dictionary (after adding key-value pairs).
    """

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
    """
    Parses the number of nucleons present in an element. It adds a key in
    the dictionary passed as parameter - 'Nucleons'. This entry exists in
    the third `<td>` tag, in every record of table, no checks are required.

    :param row_data: list of `<td>` tags in a single row.
    :param df_record: existing dictionary containing already parsed entries.
    :return: Modified dictionary (after adding key-value pair).
    """

    df_record["Nucleons"] = int(tu.unicode_to_utf8(row_data[2].text))

    return df_record


def parse_relative_atomic_mass(row_data, df_record):
    """
    Parses relative atomic mass of the isotope. It adds a key in the dictionary
    passed as parameter - 'Relative Atomic Mass'. This entry exists in the
    fourth `<td>` tag, in a particular record of table, it might be absent so
    try-except block is required.

    :param row_data: list of `<td>` tags in a single row.
    :param df_record: existing dictionary containing already parsed entries.
    :return: Modified dictionary (after adding key-value pairs).
    """

    relative_atomic_mass = tu.parse_float(row_data[3].text)
    df_record["Relative Atomic Mass"] = relative_atomic_mass

    return df_record


def parse_isotopic_composition(row_data, df_record):
    """
    Parses isotopic composition of the isotope. It adds a key in the dictionary
    passed as parameter - 'Isotopic Composition'. This entry exists in the
    fifth `<td>` tag, in a particular record of table, it might be absent so
    try-except block is required.

    :param row_data: list of `<td>` tags in a single row.
    :param df_record: existing dictionary containing already parsed entries.
    :return: Modified dictionary (after adding key-value pairs).
    """

    try:
        isotopic_composition = tu.parse_float(row_data[4].text)
        df_record["Isotopic Composition"] = isotopic_composition
    except ValueError:
        df_record["Isotopic Composition"] = None

    return df_record


def parse_std_atomic_weight_and_notes(row, df_record):
    """
    * Parses the standard atomic weight chosen for element, which is chosen
      among atomic weight of all its isotopes. It adds a key in the dictionary
      passed as parameter - 'Standard Atomic Weight'. Also parses any
      additional notes is present and adds a key - 'Notes'.
    * These entries exist in the last two `<td>` tags, in the record
      containing first isotope of the corresponding element.

    :param row: single `<tr>` tag containing a single record of the table.
    :param df_record: existing dictionary containing already parsed entries.
    :return: Modified dictionary (after adding key-value pair).
    """

    std_atomic_weight = row.find_next_sibling("td")

    if std_atomic_weight is not None:
        text = tu.parse_float_list(std_atomic_weight.text)
        df_record["Standard Atomic Weight"] = str(text)

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
    atomic_dataset = fetch_atomic_dataset()
    atomic_dataset.to_csv("bin/dataset.csv", index=False)
    dbu.databrame_to_sql_table(atomic_dataset)
