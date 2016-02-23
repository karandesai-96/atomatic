import requests
from bs4 import BeautifulSoup


def get_soup_from_url(url):
    """
    Makes a GET request to the url and create a BeautifulSoup from its
    request response content.

    :param url: url of web page.
    :return: soup: BeautifulSoup made from url request response content.
    """

    req = requests.get(url, timeout=3)
    soup = BeautifulSoup(req.content, "html.parser")

    return soup


def get_soup_from_file(filename):
    """
    Creates a BeautifulSoup by taking in the contents from an html file as
    markup.

    :param filename: name of html file located in outdump/ directory
    :return: soup: BeautifulSoup made from file contents as markup.
    """

    content_file = open("outdump/" + filename, "r+")
    content = content_file.read()
    soup = BeautifulSoup(content, "html.parser")
    content_file.close()

    return soup


def store_content_from_url(url, filename):
    """
    Makes a GET request to the url and write the request response content in
    a file, and saves it under outdump/ directory.

    :param url: url of web page.
    :param filename: name of file to be saved.
    :return: None
    """

    req = requests.get(url, timeout=3)
    content_file = open("outdump/" + filename, "w+")
    content_file.write(req.content)
    content_file.close()


def store_content_from_soup(soup, filename):
    """
    Writes the content of a BeautifulSoup in a file and saves it under
    outdump/ directory.

    :param soup: BeautifulSoup whose content is to be written.
    :param filename: name of file to be saved.
    :return: None
    """

    content = str(soup)
    content_file = open("outdump/" + filename, "w+")
    content_file.write(content)
    content_file.close()
