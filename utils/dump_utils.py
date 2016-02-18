import requests
from bs4 import BeautifulSoup


def get_soup_from_url(url):
    req = requests.get(url, timeout=3)
    soup = BeautifulSoup(req.content, "html.parser")

    return soup


def get_soup_from_file(filename):
    content_file = open("outdump/" + filename, "r+")
    content = content_file.read()
    soup = BeautifulSoup(content, "html.parser")
    content_file.close()

    return soup


def store_content_from_url(url, filename):
    req = requests.get(url, timeout=3)
    content_file = open("outdump/" + filename, "w+")
    content_file.write(req.content)
    content_file.close()


def store_content_from_soup(soup, filename):
    content = str(soup)
    content_file = open("outdump/" + filename, "w+")
    content_file.write(content)
    content_file.close()
