from utils import soup_utils as su
from utils import text_utils as tu


def fetch_atomic_dataset():
    url = "http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"

    physics_nist_soup = su.get_soup_from_url(url)
    headings = fetch_table_headings(physics_nist_soup)

    return


def fetch_table_headings(soup):
    headings = list()

    for heading in soup.find_all("th", attrs={'valign': 'bottom'}):
        headings.append(heading.text)

    for i in range(len(headings)):
        headings[i] = tu.unicode_to_utf8(headings[i])
        headings[i] = tu.beautify_text(headings[i])

    return headings
