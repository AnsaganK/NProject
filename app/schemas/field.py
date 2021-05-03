from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from pydantic.types import List


class FieldSchema(BaseModel):
    name: Optional[str] = Field(None)
    kadNumber: str
    organizationId: int
    urlShpFile: Optional[str] = Field(None)
    shapeId: Optional[int] = Field(None)
    districtId: Optional[str] = Field(None)
    typeId: Optional[int] = Field(None)
    area: dict
    length: float
    geoJson: dict
