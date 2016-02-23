import unicodedata


def unicode_to_utf8(text):
    """
    Converts unicode string to utf8 string. Text from an html tag is
    available as unicode string.
    * Example : u'sample text' => "sample text"

    :param text: unicode string
    :return: text: utf8 string
    """

    text = unicodedata.normalize("NFKD", text).encode("utf-8", "ignore")
    text = text.strip()
    return text


def beautify_text(text):
    """
    Removes Trailing spaces, provides single spaces before capitalizations.
    * Example : "   SampleText  Foo   Bar " => "Sample Text Foo Bar"

    :param text: string with inconsistent spacing
    :return: beautified_text: formatted string as described
    """

    words = text.split()
    no_spaces_text = ""
    for word in words:
        if word != "":
            no_spaces_text += word

    beautified_text = ""
    for i in range(len(no_spaces_text)):
        if 'A' <= no_spaces_text[i] <= 'Z':
            beautified_text += " " + no_spaces_text[i]
        else:
            beautified_text += no_spaces_text[i]
    beautified_text = beautified_text.strip()

    return beautified_text


def parse_float(num_str):
    """
    Parses a string representing a decimal number to float. The available
    data also has certain parenthesis which can be skipped out, so stray
    whitespaces and parenthesis are taken care of.
    * Example : "28.111 996 4(23)" => 28.1119964

    :param num_str: string representing a decimal number
    :return: num_str: float obtained as described
    """

    num_str = unicode_to_utf8(num_str)
    num_str = float(num_str.replace(' ', '').split('(')[0])
    return num_str


def parse_float_list(list_str):
    """
    Uses parse_float method to parse a string representing a list of decimal
    numbers to a list of float.
    * Example : "  [2.300 123 6, 8.234 54(80)] " => [2.3001236, 8.23454]

    :param list_str: string representing list of decimal numbers
    :return: if only one element, then the number itself, else a list of floats
    """

    list_str = list_str.replace(' ', '')
    list_str = list_str.replace('[', '')
    list_str = list_str.replace(']', '')
    num_strs = list_str.split(',')

    for _ in range(len(num_strs)):
        num_strs[_] = parse_float(num_strs[_])

    if len(num_strs) == 1:
        return num_strs[0]
    return num_strs
