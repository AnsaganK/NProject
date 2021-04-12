from enum import Enum

from pydantic import BaseModel

class ActionName(str, Enum):
    created = "Создано"
    edited = "Изменено"
    deleted = "Удалено"


class HistoryFieldsSchema(BaseModel):
    fieldId: int
    action: ActionName
    userId: int
    date: int


class CreateHistoryFieldsSchema(HistoryFieldsSchema):
    id: int

    class Config:
        orm_mode = True
