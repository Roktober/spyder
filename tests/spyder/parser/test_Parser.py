from spyder.parser.Parser import Parser
from spyder.parser.data.Data import Data

urls_expected = {"http://test.com/go0", "http://test.com/go1/",
                 "http://test.com/go2", "http://go2.ru"}


def test_Parser_parse_1(source_html, url, html_title):
    data: Data = Parser.parse(source_html, url)
    assert data.urls == urls_expected
    assert data.html == source_html
    assert data.title == html_title
    assert data.uri == url
