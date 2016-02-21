import utils.text_utils as tu


def test_unicode_to_utf8():
    utf8_text = tu.unicode_to_utf8(u'test text')
    assert type(utf8_text) is str
    assert utf8_text == "test text"


def test_beautify_text():
    beautified_text = tu.beautify_text("  Test Text ")
    assert beautified_text == "Test Text"

    beautified_text = tu.beautify_text("TestText Test   Text  ")
    assert beautified_text == "Test Text Test Text"


def test_parse_float():
    parsed_float = tu.parse_float(u'2.002 134 24')
    assert parsed_float == 2.00213424

    parsed_float = tu.parse_float(u'0.012 32(70)')
    assert parsed_float == 0.01232
