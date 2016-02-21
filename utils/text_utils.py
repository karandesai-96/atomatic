import unicodedata


def unicode_to_utf8(text):
    text = unicodedata.normalize("NFKD", text).encode("utf-8", "ignore")
    text = text.strip()
    return text


def beautify_text(text):
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
    num_str = unicode_to_utf8(num_str)
    num_str = num_str.replace(' ', '').split('(')[0]
    return float(num_str)


def parse_float_list(list_str):
    list_str = list_str.replace(' ', '')
    list_str = list_str.replace('[', '')
    list_str = list_str.replace(']', '')
    num_strs = list_str.split(',')

    for _ in range(len(num_strs)):
        num_strs[_] = parse_float(num_strs[_])

    return num_strs
