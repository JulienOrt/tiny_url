import random
import string

from fastapi import status
from pydantic import HttpUrl

from tiny_url.models.exceptions import TinyUrlBaseException


class UrlController:
    @staticmethod
    def generate_slug_url(tiny_url_len: int) -> str:
        if not (0 < tiny_url_len < 101):
            raise TinyUrlBaseException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, message="Tiny Url must be of len between 1 and 100")

        characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
        return ''.join(random.choices(characters, k=tiny_url_len))

    @staticmethod
    def verify_url(input_url: str) -> None:
        """
        Verifies whether the input url has a decent format

        Args:
            input_url (str): url to be tested

        Raises:
            TinyUrlBaseException: in case the url has a wrong format
        """

        try:
            HttpUrl(url=input_url)
        except Exception:
            TinyUrlBaseException(message=f"Input url is not a valid url: {input_url}", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
