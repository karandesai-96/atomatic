from utils import soup_utils as su


def fetch_atomic_dataset():
    url = "http://physics.nist.gov/cgi-bin/Compositions/stand_alone.pl"

    physics_nist_soup = su.get_soup_from_url(url)

    for header in physics_nist_soup.find_all("th", attrs={'valign': 'bottom'}):
        print "HEADER ......."
        print header.text
        print type(header.text)

    return
