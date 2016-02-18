from utils import soup_utils as su
import unicodedata


def fetch_atomic_dataset():
    url = "http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"

    physics_nist_soup = su.get_soup_from_url(url)
    headings = fetch_table_headings(physics_nist_soup)

    return


def fetch_table_headings(soup):
    headings = list()

    for heading in soup.find_all("th", attrs={'valign': 'bottom'}):
        headings.append(heading.text)

    return headings
