from urllib.parse import urlparse

from spyder.parser.URLProcessor import URLProcessor

urls_expected = ["http://test.com/go0", "http://test.com/go1/",
                 "http://test.com/go2", None, "http://go2.ru"]


def test_URLProcessor_parse_1(url, html_href):
    url = urlparse(url)
    res_list = []
    for u in html_href:
        res = URLProcessor.parse(url, u)
        res_list.append(res)
    assert res_list == urls_expected


def test_URLProcessor_process_urls_1(url, html_href):
    url = urlparse(url)
    res = URLProcessor.process_urls(url, html_href)
    assert res == set(filter(lambda u: u is not None, urls_expected))
