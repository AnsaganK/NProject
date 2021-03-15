from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from pydantic.types import List


class FieldSchema(BaseModel):
    name: Optional[str] = Field(None)
    kadNumber: str
    organizationId: int
    urlShpFile: Optional[str] = Field(None)
    districtId: Optional[str] = Field(None)
    GeoJson: dict
