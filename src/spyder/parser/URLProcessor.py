import logging
import urllib.parse
import os
import re


class URLProcessor:
    """
    Build and filter url for query
    """
    logger = logging.getLogger(__name__)

    ALLOW_SCHEME = ("http", "https")
    AVOID_HTML_LINK_PATTERN = re.compile("#.*")
    ALLOW_ANOTHER_NETLOC = True
    ALLOW_LINK_TYPE = (".html", ".php")

    @staticmethod
    def parse(base_url: urllib.parse.ParseResult, url: str) -> str:
        if "#" in url:
            url = URLProcessor.AVOID_HTML_LINK_PATTERN.sub(url, "")

        parsed_url = urllib.parse.urlparse(url)

        if parsed_url.scheme and \
                parsed_url.scheme not in URLProcessor.ALLOW_SCHEME:
            return None

        _, link_type = os.path.splitext(parsed_url.path)
        if link_type:
            if link_type.lower() not in URLProcessor.ALLOW_LINK_TYPE:
                URLProcessor.logger.warning(f"Skip url: {url}")
                return None

        if not URLProcessor.ALLOW_ANOTHER_NETLOC and parsed_url.netloc:
            if parsed_url.netloc == base_url.netloc:
                return urllib.parse.urljoin(base_url.geturl(),
                                            parsed_url.geturl())
            else:
                return None

        return urllib.parse.urljoin(base_url.geturl(), parsed_url.geturl())

    @staticmethod
    def process_urls(base_url: urllib.parse.ParseResult, urls: set) -> set:
        return set(filter(lambda u:
                          u is not None,
                          map(lambda u:
                              URLProcessor.parse(base_url, u), urls)))
