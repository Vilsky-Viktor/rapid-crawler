import pymongo
from typing import List, Optional
from rapid_scrawler.config import Config
from rapid_scrawler.models.post import PostModel


class PostsTable:
    def __init__(self) -> None:
        self.db = None
        self.collection = None

    def set_client(self) -> None:
        try:
            self.db = pymongo.MongoClient(Config.DB_CONN_STR, directConnection=True)
            self.collection = self.db.crawler.posts
        except Exception as error:
            raise Exception(f"database error: {str(error)}")

    def insert_many(self, posts: List[PostModel]) -> None:
        if posts:
            converted = [vars(post) for post in posts]
            self.collection.insert_many(converted)

    def get_latest_item(self, url: str) -> Optional[PostModel]:
        res = self.collection.find_one(
            {"url": url}, sort=[("date", pymongo.DESCENDING)]
        )
        if res:
            return PostModel(
                res["url"],
                res["post_url"],
                res["title"],
                res["content"],
                res["user"],
                res["date"],
            )
        return None
