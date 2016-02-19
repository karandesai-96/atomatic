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
    return
