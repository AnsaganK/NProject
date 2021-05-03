from pydantic import BaseModel
from pydantic.types import Optional


class ShapeSchema(BaseModel):
    geoJson: Optional[dict] = None
    url: str


class ShapeCreateSchema(ShapeSchema):
    id: int
