from utils import soup_utils as su
from utils import text_utils as tu
import os
import pandas as pd


def fetch_atomic_dataset():
    url = "http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"

    if os.path.isfile("mainsoup.html"):
        physics_nist_soup = su.get_soup_from_file("mainsoup.html")
    else:
        physics_nist_soup = su.get_soup_from_url(url)
        su.store_content_from_soup(physics_nist_soup, filename="mainsoup.html")

    headings = ["Z", "Symbol", "Nucleons", "Relative Atomic Mass", "Isotopic \
                Composition", "Standard Atomic Weight", "Notes"]

    atomic_dataset = pd.DataFrame(columns=headings)

    rows = physics_nist_soup.find_all("tr")

    # boilerplate code for quick debugging assistance
    for _ in range(4, 20):
        df_record = fetch_row(rows[_])
        if df_record["Symbol"] is not None:
            print df_record
    return


# incomplete
def fetch_row(row):
    df_record = dict()

    row_data = row.find_all("td")

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
        # dummy elements in row_data : Z at index 0 and symbol at index 1
        row_data.insert(0, None)
        row_data.insert(1, None)

    # this condition is only for H, D, T records in the whole table
    # D, T will be third entry in list due to dummy entries added in else block
    if row_data[2].get("align") == "center":
        df_record["Symbol"] = tu.unicode_to_utf8(row_data[2].text)
        row_data.pop(1)

    return df_record
