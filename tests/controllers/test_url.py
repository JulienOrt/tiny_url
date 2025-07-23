import pytest

from tiny_url.controllers.url import UrlController
from tiny_url.models.exceptions import TinyUrlBaseException


class TestSlugUrl:
    @staticmethod
    def test_basic():

        for url_len in [i for i in range(1, 50)]:
            slug_url = UrlController.generate_slug_url(tiny_url_len=url_len)
            assert len(slug_url) == url_len

    @staticmethod
    def test_min_limit():
        with pytest.raises(expected_exception=TinyUrlBaseException, match="Tiny Url must be of len between 1 and 100"):
            UrlController.generate_slug_url(tiny_url_len=-1)

    @staticmethod
    def test_max_limit():
        with pytest.raises(expected_exception=TinyUrlBaseException, match="Tiny Url must be of len between 1 and 100"):
            UrlController.generate_slug_url(tiny_url_len=200)
