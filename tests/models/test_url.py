from datetime import datetime, UTC

from tiny_url.models.url import SlugUrl


def test_slug_url():
    slug_id = 123
    source_url = "test_source_url"
    slug_url = "test_slug_url"
    end_validity_date = datetime.now(UTC)

    slug = SlugUrl(
        id=slug_id,
        source_url=source_url,
        slug_url=slug_url
    )

    assert slug is not None
    assert isinstance(slug, SlugUrl)
    assert slug.id == slug_id
    assert slug.source_url == source_url
    assert slug.slug_url == slug_url
    assert slug.end_validity_date is None

    slug = SlugUrl(
        id=slug_id,
        source_url=source_url,
        slug_url=slug_url,
        end_validity_date=end_validity_date
    )
    assert slug.end_validity_date == end_validity_date
