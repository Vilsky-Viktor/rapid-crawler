from rapid_scrawler.validators.url import is_valid_url


def test_is_valid_url_http():
    url = "http://test.com"
    assert is_valid_url(url) is True


def test_is_valid_url_https():
    url = "https://test.com"
    assert is_valid_url(url) is True


def test_is_valid_url_localhost():
    url = "http://localhost"
    assert is_valid_url(url) is True


def test_is_valid_url_port():
    url = "http://localhost:4000"
    assert is_valid_url(url) is True


def test_is_valid_url_invalid():
    url = "abc"
    assert is_valid_url(url) is False


def test_is_valid_url_invalid2():
    url = "https://test"
    assert is_valid_url(url) is False
