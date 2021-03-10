from pydantic import BaseModel, HttpUrl
from typing import Optional
from pydantic.types import List


class FieldSchema(BaseModel):
    name: str
    kadNumber: str
    organizationId: int
    urlShpFile: str
    districtId: str
