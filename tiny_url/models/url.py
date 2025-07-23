from typing import Optional

from pydantic import BaseModel, Field, AwareDatetime


class SlugUrl(BaseModel):
    id: int = Field(description="Database ID")
    source_url: str = Field(description="Source URL attached to the slug url")
    slug_url: str = Field(description="Slug url")
    end_validity_date: Optional[AwareDatetime] = Field(default=None, description="End validity date of the slug URL")
