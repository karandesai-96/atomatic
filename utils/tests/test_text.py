import utils.text_utils as tu


def test_unicode_to_utf8():
    utf8_text = tu.unicode_to_utf8(u'test text')
    assert type(utf8_text) is str
    assert utf8_text == "test text"


def test_beautify_text():
    pass
