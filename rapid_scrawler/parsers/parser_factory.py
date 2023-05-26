from urllib.parse import urlparse
from rapid_scrawler.parsers.pastebincom_parser import PastebincomParser

PARSER_MAP = {"https://pastebin.com/archive": PastebincomParser}


class ParserFactory:
    def __init__(self, url: str) -> None:
        self.url = url

    def _get_base_url(self) -> str:
        try:
            parsed_url = urlparse(self.url)
            return f"{parsed_url.scheme}://{parsed_url.netloc}"
        except Exception:
            raise Exception(f"url is not valid: {self.url}")

    def create_parser(self) -> any:
        base_url = self._get_base_url()
        class_name = PARSER_MAP.get(self.url, None)
        if class_name:
            return class_name(self.url, base_url)
        else:
            raise Exception(f"post parser is not supported for {self.url}")
