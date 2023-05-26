from lxml import html
from lxml.etree import _Element
from rapid_crawler.parsers.pastebincom_parser import PastebincomParser


def test_get_post_urls():
    with open("tests/mock_data/pastebincom_html/archive.html") as file:
        contents = file.read()
        page_tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        parser = PastebincomParser(url, base_url)
        parser._get_post_urls(page_tree)
        assert parser.post_urls == [f"{base_url}/1", f"{base_url}/2"]


def test_get_post_urls_error():
    with open("tests/mock_data/pastebincom_html/blank_page.html") as file:
        contents = file.read()
        page_tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        parser = PastebincomParser(url, base_url)
        try:
            parser._get_post_urls(page_tree)
        except Exception as error:
            assert str(error) == f"could not parse post urls for {url}"


def test_get_post_info_block():
    with open("tests/mock_data/pastebincom_html/post_page.html") as file:
        contents = file.read()
        page_tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        info_tree = parser._get_post_info_block(page_tree, post_url)
        print(info_tree)
        assert isinstance(info_tree, _Element)


def test_get_post_info_block_error():
    with open("tests/mock_data/pastebincom_html/blank_page.html") as file:
        contents = file.read()
        page_tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        try:
            parser._get_post_info_block(page_tree, post_url)
        except Exception as error:
            assert str(error) == f"info block is not found ({post_url})"


def test_get_post_title():
    with open("tests/mock_data/pastebincom_html/title_block.html") as file:
        contents = file.read()
        tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        title = parser._get_post_title(tree, post_url)
        assert title == "Test title"


def test_get_post_title_untitled():
    with open("tests/mock_data/pastebincom_html/title_block_undefined.html") as file:
        contents = file.read()
        tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        title = parser._get_post_title(tree, post_url)
        assert title == ""


def test_get_post_title_error():
    with open("tests/mock_data/pastebincom_html/blank_page.html") as file:
        contents = file.read()
        tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        try:
            parser._get_post_title(tree, post_url)
        except Exception as error:
            assert str(error) == f"title is not found ({post_url})"


def test_get_post_date():
    with open("tests/mock_data/pastebincom_html/date_block.html") as file:
        contents = file.read()
        tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        date = parser._get_post_date(tree, post_url)
        assert date == "2023-05-26T09:03:55+00:00"


def test_get_post_date_error():
    with open("tests/mock_data/pastebincom_html/blank_page.html") as file:
        contents = file.read()
        tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        try:
            parser._get_post_date(tree, post_url)
        except Exception as error:
            assert str(error) == f"date is not found ({post_url})"


def test_get_post_user():
    with open("tests/mock_data/pastebincom_html/user_block.html") as file:
        contents = file.read()
        tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        user = parser._get_post_user(tree, post_url)
        assert user == "test_user"


def test_get_post_user_untitled():
    with open("tests/mock_data/pastebincom_html/user_block_undefined.html") as file:
        contents = file.read()
        tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        user = parser._get_post_user(tree, post_url)
        assert user == ""


def test_get_post_user_error():
    with open("tests/mock_data/pastebincom_html/blank_page.html") as file:
        contents = file.read()
        tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        try:
            parser._get_post_user(tree, post_url)
        except Exception as error:
            assert str(error) == f"user name is not found ({post_url})"


def test_get_post_content():
    with open("tests/mock_data/pastebincom_html/content_block.html") as file:
        contents = file.read()
        tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        content = parser._get_post_content(tree, post_url)
        assert content == "first line\nsecond line"


def test_get_post_content_error():
    with open("tests/mock_data/pastebincom_html/blank_page.html") as file:
        contents = file.read()
        tree = html.fromstring(contents)
        base_url = "http://test.com"
        url = f"{base_url}/archive"
        post_url = f"{base_url}/1"
        parser = PastebincomParser(url, base_url)
        try:
            parser._get_post_content(tree, post_url)
        except Exception as error:
            assert str(error) == f"content is not found ({post_url})"
