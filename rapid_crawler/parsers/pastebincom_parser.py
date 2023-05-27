import dateparser
import arrow
from rapid_crawler.models.post import PostModel
from rapid_crawler.parsers.parser_base import ParserBase
from rapid_crawler.config import Config
from lxml.etree import _ElementTree


class PastebincomParser(ParserBase):
    def __init__(self, url: str, base_url: str) -> None:
        super().__init__(url, base_url)

    def _get_post_urls(self, page_tree: _ElementTree) -> None:
        try:
            table = page_tree.cssselect("table")[0]
            for row in table.cssselect("tr")[1:]:
                title_cell = row.cssselect("td")[0]
                path = title_cell.cssselect("a")[0].get("href")
                post_url = f"{self.base_url}{path}"
                self.post_urls.append(post_url)
        except Exception:
            raise Exception(f"could not parse post urls for {self.url}")

    async def _get_post_data(self, post_url: str) -> None:
        page_tree = await self._get_page_tree(post_url)
        info_tree = self._get_post_info_block(page_tree, post_url)
        title = self._get_post_title(info_tree, post_url)
        date = self._get_post_date(info_tree, post_url)
        user = self._get_post_user(info_tree, post_url)
        content = self._get_post_content(page_tree, post_url)
        post = PostModel(self.url, post_url, title, content, user, date)
        self.posts.append(post)

    def _get_post_info_block(self, tree: _ElementTree, post_url: str) -> _ElementTree:
        try:
            return tree.cssselect(".details div.info-bar")[0]
        except Exception:
            raise Exception(f"info block is not found ({post_url})")

    def _get_post_title(self, tree: _ElementTree, post_url: str) -> str:
        try:
            value = tree.cssselect("h1")[0].text_content().strip()
            if value.lower() in Config.UNDEFINED_VALUES:
                return ""
            return value
        except Exception:
            raise Exception(f"title is not found ({post_url})")

    def _get_post_date(self, tree: _ElementTree, post_url: str) -> str:
        try:
            date_str = tree.cssselect(".date > span")[0].get("title")
            date = dateparser.parse(date_str)
            date_obj = arrow.get(date)
            return str(date_obj.to("UTC"))
        except Exception:
            raise Exception(f"date is not found ({post_url})")

    def _get_post_user(self, tree: _ElementTree, post_url: str) -> str:
        try:
            value = tree.cssselect(".username a")[0].text_content().strip()
            if value.lower() in Config.UNDEFINED_VALUES:
                return ""
            return value
        except Exception:
            raise Exception(f"user name is not found ({post_url})")

    def _get_post_content(self, tree: _ElementTree, post_url: str) -> str:
        try:
            content_tree = tree.cssselect("div.source ol li")
            content_arr = []
            for line in content_tree:
                line_arr = line.text_content().strip().split("\n")
                stripped_line_arr = [line.strip() for line in line_arr]
                stripped_line = " ".join(stripped_line_arr)
                content_arr.append(stripped_line)
            return "\n".join(content_arr)
        except Exception:
            raise Exception(f"content is not found ({post_url})")
