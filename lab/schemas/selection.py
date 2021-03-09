from pydantic import BaseModel
from .samples import SamplesSchema
from enum import Enum
from app.schemas.organization import OrganizationSchema


class StatusName(str, Enum):
    received = "received"
    during = "during"
    done = "done"


class SelectionSchema(BaseModel):
    name: OrganizationSchema
    samples: SamplesSchema
    amount: int
    date: int
    status: StatusName
