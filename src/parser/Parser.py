from .data import Data

from lxml import html
import urllib.parse
import re
import logging


class Parser:
    logger = logging.getLogger(__name__)

    @staticmethod
    def parse(source_html: str, url: str) -> Data:
        data: Data = None
        try:
            base_url = urllib.parse.urlparse(url)
            data = HTMLParser.parse(source_html, url)
            data.urls = URLParser.process_urls(base_url, data.urls)
        except Exception as e:
            Parser.logger.error(f"Parse error url: {url}", exc_info=True)
        return data


class HTMLParser:
    @staticmethod
    def parse(source_html: str, url: str) -> Data:
        parsed_html = html.fromstring(source_html)
        title = parsed_html.xpath('//title/text()')
        if len(title) < 1:
            title = ""
            Parser.logger.warning(f"URL: {url} haven't title")
        else:
            title = title[0]
        urls = set(parsed_html.xpath('//a/@href'))
        title_data = Data.Data(source_html, url, title, urls)
        return title_data


class URLParser:
    ALLOW_SCHEME = ("http", "https")
    AVOID_HTML_LINK_PATTERN = re.compile("#.*")
    ALLOW_ANOTHER_NETLOC = True

    @staticmethod
    def parse(base_url: urllib.parse.ParseResult, url: str) -> str:
        if "#" in url:
            url = URLParser.AVOID_HTML_LINK_PATTERN.sub(url, "")

        parsed_url = urllib.parse.urlparse(url)

        if parsed_url.scheme not in URLParser.ALLOW_SCHEME:
            return None

        if not URLParser.ALLOW_ANOTHER_NETLOC and parsed_url.netloc:
            if parsed_url.netloc == base_url.netloc:
                return urllib.parse.urljoin(base_url.geturl(),
                                            parsed_url.geturl())
            else:
                return None

        return urllib.parse.urljoin(base_url.geturl(), parsed_url.geturl())

    @staticmethod
    def process_urls(base_url: urllib.parse.ParseResult, urls: set) -> set:
        return set(filter(lambda u: u is not None,
                          map(lambda u: URLParser.parse(base_url, u), urls)))
