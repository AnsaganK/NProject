from pydantic import BaseModel
from pydantic.types import List, Optional


class ErrorRangeSchema(BaseModel):
    of: float
    to: float
    percent: float