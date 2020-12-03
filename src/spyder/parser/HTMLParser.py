import logging
from typing import List

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

from .data import Data


class HTMLParser:
    logger = logging.getLogger(__name__)
    TITLE_TAG = SoupStrainer("title")
    A_TAG = SoupStrainer("a", href=True)

    @staticmethod
    def parse(source_html: str, url: str) -> Data:
        """
        Parse a.href, title from html with lxml backend, ignore other tags
        :param source_html:
        :param url:
        :return:
        """
        title = HTMLParser._parse_title(source_html, url)
        urls = set(HTMLParser._parse_href_from_a(source_html, url))
        title_data = Data.Data(source_html, url, title, urls)
        return title_data

    @staticmethod
    def _parse_title(source_html: str, url: str) -> str:
        """
        Parse only title tag
        :param source_html:
        :param url:
        :return: title if present else None
        """
        title_bs = BeautifulSoup(source_html, "lxml",
                                 parse_only=HTMLParser.TITLE_TAG)
        title = None
        if title_bs.title:
            title = title_bs.title.text
        else:
            HTMLParser.logger.warning(f"URL: {url} haven't title")
        return title

    @staticmethod
    def _parse_href_from_a(source_html: str, url: str) -> List[str]:
        """
        Parse only title tag
        :param source_html:
        :param url:
        :return: list of href if present else empty list
        """
        a_bs = BeautifulSoup(source_html, "lxml",
                             parse_only=HTMLParser.A_TAG)
        urls = [a.get("href") for a in a_bs.find_all("a")]
        if not urls:
            HTMLParser.logger.warning(f"URL: {url} haven't links")
        return urls
