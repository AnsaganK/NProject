from fastapi import APIRouter
from db import session
from app.models.workType import WorkType
from app.models.workSubType import WorkSubType
from app.schemas.workSubType import workSubTypeSchema, createWorkSubTypeSchema
from app.schemas import ErrorSchema
from typing import Union
from sqlalchemy.orm import selectinload

router = APIRouter()

@router.get("")
async def get_work_sub_types():
    query = session.query(WorkSubType).options(selectinload(WorkSubType.group)).all()
    return query

@router.post("", response_model=Union[createWorkSubTypeSchema, ErrorSchema])
async def create_work_sub_type(workSubType: workSubTypeSchema):
    query = WorkSubType(name=workSubType.name, description=workSubType.description, default=workSubType.default)
    group = session.query(WorkType).get(workSubType.groupId)
    if not group:
        return {"error": "Не найден тип работы"}

    query.group = group

    session.add(query)
    session.commit()
    return query



@router.get("/{workSubType_id}")
async def get_detail_work_type(workSubType_id: int):
    query = session.query(WorkSubType).get(workSubType_id)
    if query:
        return query
    return {"error": "Такой объект не найден"}

@router.delete("/{workSubType_id}")
async def delete_work_type(workSubType_id: int):
    query = session.query(WorkSubType).get(workSubType_id)
    if query:
        session.add(query)
        session.commit()
        return {"message": "deleted"}
    return {"error": "Такой объект не существует"}