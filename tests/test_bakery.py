import pytest

from downloader import is_youtube_url


@pytest.mark.parametrize(
    "url",
    [
        "https://www.youtube.com/watch?v=abc123",
        "https://youtu.be/abc123",
        "http://m.youtube.com/watch?v=abc123",
    ],
)
def test_accepts_youtube_urls(url):
    assert is_youtube_url(url)


@pytest.mark.parametrize("url", ["", "https://example.com/video", "not a url"])
def test_rejects_non_youtube_urls(url):
    assert not is_youtube_url(url)
