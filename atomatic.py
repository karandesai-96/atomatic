from utils import soup_utils as su
from utils import text_utils as tu
import pandas as pd


def fetch_atomic_dataset():
    url = "http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"

    physics_nist_soup = su.get_soup_from_url(url)
    headings = ["Z", "Symbol", "Nucleons", "Relative Atomic Mass", "Isotopic \
                Composition", "Standard Atomic Weight", "Notes"]

    atomic_dataset = pd.DataFrame(columns=headings)

    rows = physics_nist_soup.find_all("tr")
    return
