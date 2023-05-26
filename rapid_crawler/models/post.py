class PostModel:
    def __init__(
        self,
        url: str,
        post_url: str,
        title: str,
        content: str,
        user: str,
        date: str,
    ) -> None:
        self.url = url
        self.post_url = post_url
        self.title = title
        self.content = content
        self.user = user
        self.date = date
