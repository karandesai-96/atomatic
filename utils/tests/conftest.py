import pytest
import base64


mountain = open("/home/darth_sidious/Desktop/mountain.png").read()
mountain_enc = base64.b64encode(mountain)


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        if report.nodeid.split("::")[-1] == "test_beautify_text":
            print "HOORAY"
            extra.append(pytest_html.extras.image(mountain_enc))
        report.extra = extra
