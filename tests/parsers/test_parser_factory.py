from rapid_scrawler.parsers.parser_factory import ParserFactory
from rapid_scrawler.parsers.pastebincom_parser import PastebincomParser


def test_get_base_url():
    url = "https://test.com/page"
    factory = ParserFactory(url)
    base_url = factory._get_base_url()
    assert base_url == "https://test.com"


def test_get_base_url_subdomain():
    url = "https://sub.test.com/page"
    factory = ParserFactory(url)
    base_url = factory._get_base_url()
    assert base_url == "https://sub.test.com"


def test_get_base_url_localhost():
    url = "http://localhost/page"
    factory = ParserFactory(url)
    base_url = factory._get_base_url()
    assert base_url == "http://localhost"


def test_get_base_url_port():
    url = "http://localhost:4000/page"
    factory = ParserFactory(url)
    base_url = factory._get_base_url()
    assert base_url == "http://localhost:4000"


def test_get_base_url_error():
    url = 123
    factory = ParserFactory(url)
    try:
        factory._get_base_url()
    except Exception as error:
        assert str(error) == "url is not valid: 123"


def test_create_parser():
    url = "https://pastebin.com/archive"
    factory = ParserFactory(url)
    parser = factory.create_parser()
    assert isinstance(parser, PastebincomParser)


def test_create_parser_not_supported():
    url = "https://test.com/archive"
    factory = ParserFactory(url)
    try:
        factory.create_parser()
    except Exception as error:
        assert str(error) == f"post parser is not supported for {url}"
