import os
from bs4 import BeautifulSoup
import utils.soup_utils as su

test_url = "http://www.ismycomputeron.com"

req_response = '<html><body bgcolor="FFFFFF"><center>' \
         '<font type="ariel" size="4">YES</font>' \
         '</center></body></html>'

markup = '<html><body bgcolor="FFFFFF"><center>' \
         '<font size="4" type="ariel">YES</font>' \
         '</center></body></html>'

test_soup = BeautifulSoup(markup, "html.parser")


def test_get_soup_from_url():
    soup = su.get_soup_from_url(test_url)
    assert soup == test_soup


def test_get_soup_from_file():
    # setup
    test_file = open("outdump/test.html", "w+")
    test_file.write(markup)
    test_file.close()

    soup = su.get_soup_from_file("test.html")
    assert soup == test_soup

    # teardown
    os.remove("outdump/test.html")


def test_store_content_from_url():
    su.store_content_from_url(test_url, "test.html")
    assert os.path.isfile("outdump/test.html")

    test_file = open("outdump/test.html")
    content = test_file.read()
    test_file.close()
    assert content == req_response

    # teardown
    os.remove("outdump/test.html")


def test_store_content_from_soup():
    su.store_content_from_soup(test_soup, "test.html")
    assert os.path.isfile("outdump/test.html")

    test_file = open("outdump/test.html")
    content = test_file.read()
    test_file.close()
    assert content == markup

    # teardown
    os.remove("outdump/test.html")
