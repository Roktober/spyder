from spyder.parser.HTMLParser import HTMLParser
from spyder.parser.data.Data import Data


def test_parse_title_1(source_html, url, html_title):
    title = HTMLParser._parse_title(source_html, url)
    assert title == html_title


def test_parse_href_1(source_html, url, html_href):
    urls = HTMLParser._parse_href_from_a(source_html, url)
    assert urls == html_href


def test_parse_1(source_html, url, html_href, html_title):
    data: Data = HTMLParser.parse(source_html, url)
    assert data.urls == set(html_href)
    assert data.title == html_title
    assert data.html == source_html
    assert data.uri == url
