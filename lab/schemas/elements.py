from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
from typing import Optional

class ElementsSchema(BaseModel):
    name: str
    code: str
    date: Optional[int] = Field(None)
    standard: bool = Field(default=False)
