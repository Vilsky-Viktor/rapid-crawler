from abc import ABC, abstractmethod
from logging import Logger
import asyncio
import requests
from lxml import html
from rapid_scrawler.decorators.async_timeit import async_timeit
from rapid_scrawler.db.posts import PostsTable
from lxml.etree import _ElementTree


class ParserBase(ABC):
    def __init__(self, url: str, base_url: str) -> None:
        self.db = None
        self.url = url
        self.base_url = base_url
        self.post_urls = []
        self.posts = []
        self.logger = None

    @abstractmethod
    def _get_post_urls(self, page_tree: _ElementTree):
        pass

    @abstractmethod
    def _get_post_data(self, tree: _ElementTree, post_url: str):
        pass

    @abstractmethod
    def _get_post_info_block(self, tree: _ElementTree, post_url: str):
        pass

    @abstractmethod
    def _get_post_title(self, tree: _ElementTree, post_url: str):
        pass

    @abstractmethod
    def _get_post_date(self, tree: _ElementTree, post_url: str):
        pass

    @abstractmethod
    def _get_post_user(self, tree: _ElementTree, post_url: str):
        pass

    @abstractmethod
    def _get_post_content(self, tree: _ElementTree, post_url: str):
        pass

    @async_timeit
    async def run(self) -> None:
        self.logger.info(f"parse posts for {self.url}")
        try:
            page_tree = await self._get_page_tree(self.url)
            self._get_post_urls(page_tree)
            await self._collect_new_posts()
            self.db.insert_many(self.posts)
            self.logger.info(
                f"new posts ({len(self.posts)}) have been saved for {self.url}"
            )
        except Exception as error:
            self.logger.error(
                f"did not manage to update posts for {self.url}: {str(error)}"
            )

    async def _get_page_tree(self, url: str) -> _ElementTree:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return html.fromstring(response.content)
            else:
                raise Exception(f"page error [{response.status_code}] {url}")
        except Exception:
            raise Exception(f"page is not available {url}")

    async def _collect_new_posts(self) -> None:
        latest_post = self.db.get_latest_item(self.url)
        jobs = []
        count = 1

        for post_url in self.post_urls:
            if latest_post and latest_post.post_url == post_url:
                break
            job = self._get_post_data(post_url)
            jobs.append(job)
            count += 1

        await asyncio.gather(*jobs)

    def set_db(self, db: PostsTable) -> None:
        self.db = db

    def set_logger(self, logger: Logger) -> None:
        self.logger = logger
