from pydantic import BaseModel, Field
from .samples import SamplesSchema
from enum import Enum
from app.schemas.organization import OrganizationSchema
from pydantic.types import Optional


class StatusName(str, Enum):
    planned = "planned"
    during = "during"
    done = "done"


class PreparationSchema(BaseModel):
    organization: int
    samples: int
    amount: int
    date: Optional[int] = Field(None)
    status: StatusName
