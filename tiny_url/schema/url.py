from datetime import datetime, UTC, timedelta

from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from tiny_url import APP_SETTINGS
from tiny_url.controllers.database.url_mapping import UrlMappingController
from tiny_url.controllers.url import UrlController
from tiny_url.models.exceptions import TinyUrlBaseException
from tiny_url.models.url import SlugUrl

router = APIRouter()


@router.post(path="/generate_slug", operation_id="generate_slug_url", response_model=SlugUrl)
def generate_slug_url(long_url: str, validity_duration: int = None) -> SlugUrl:
    """
    Generates a slug url for the long url in input

    Args:
        long_url (str): Input URL
        validity_duration (int): Validity duration of the slug URL (in minutes)

    Returns:
        SlugUrl: Object containing the details of the new shortened Url
    """
    # Verifies the URL
    UrlController.verify_url(input_url=long_url)

    # Slug url generation
    slug_url = UrlController.generate_slug_url(tiny_url_len=APP_SETTINGS.TINY_URL_LEN)

    # Computes the validity date
    end_validity_date = datetime.now(UTC) + timedelta(minutes=validity_duration) if validity_duration is not None else None

    # Insertion + retour de SlugUrl
    return UrlMappingController.insert_record(source_url=long_url, slug_url=slug_url, end_validity_date=end_validity_date)


@router.get(path="/{slug}", operation_id="redirect_slug_url")
def redirect(slug: str) -> RedirectResponse:
    """
    Redirects to long_url if slug_url is found

    Args:
        slug (str): slug Url

    Raises:
        TinyUrlBaseException: if slug is not found or not valid anymore

    Returns:
        RedirectResponse
    """
    # Recherche par le slug url (unique est DB)
    long_url, end_validity_date = UrlMappingController.get_long_url_by_slug_url(slug_url=slug)

    # Verification de la date de validité du tiny_url, seulement s'il est défini
    if end_validity_date is not None and datetime.now(UTC) > end_validity_date:
        raise TinyUrlBaseException(message="No slug url found", status_code=status.HTTP_404_NOT_FOUND)

    return RedirectResponse(url=long_url)
