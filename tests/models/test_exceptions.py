import pytest
from fastapi import status

from tiny_url.models.exceptions import TinyUrlBaseException


def test_tiny_url_base_exception():

    status_code = status.HTTP_409_CONFLICT
    message = "test_message"
    exc = TinyUrlBaseException(status_code=status_code, message=message)

    assert exc is not None
    assert isinstance(exc, TinyUrlBaseException)
    assert str(exc) == f"{status_code}: {message}"
    assert exc.status_code == status_code


def test_missing_status_code():
    with pytest.raises(expected_exception=TypeError, match=r"TinyUrlBaseException\.__init__\(\) missing 1 required positional argument: 'status_code'"):
        TinyUrlBaseException(message="")


def test_missing_message():
    with pytest.raises(expected_exception=TypeError, match=r"TinyUrlBaseException.__init__\(\) missing 1 required positional argument: 'message'"):
        TinyUrlBaseException(status_code=status.HTTP_404_NOT_FOUND)