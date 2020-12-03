import urllib.parse
import logging

from .data import Data
from .HTMLParser import HTMLParser
from .URLProcessor import URLProcessor


class Parser:
    """
    Parser for html and url filter
    """
    logger = logging.getLogger(__name__)

    @staticmethod
    def parse(source_html: str, url: str) -> Data:
        data: Data = None
        try:
            base_url = urllib.parse.urlparse(url)
            data = HTMLParser.parse(source_html, url)
            data.urls = URLProcessor.process_urls(base_url, data.urls)
        except Exception:
            Parser.logger.error(f"Parse error url: {url}", exc_info=True)
        return data
