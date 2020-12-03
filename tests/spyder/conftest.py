import pytest


@pytest.fixture(scope="session")
def source_html():
    with open("tests/resources/source_html.html", "r") as f:
        data = f.read()
    return data


@pytest.fixture(scope="session")
def html_href():
    return ["/go0", "/go1/", "go2", "go2.exe", "http://go2.ru"]


@pytest.fixture(scope="session")
def html_title():
    return "Title"


@pytest.fixture(scope="session")
def url():
    return "http://test.com"
