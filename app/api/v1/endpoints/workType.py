from fastapi import APIRouter
from db import session
from app.models.workType import WorkType
from app.schemas.workType import workTypeSchema, createWorkTypeSchema
from app.schemas import ErrorSchema
from typing import Union


router = APIRouter()

@router.get("")
async def get_work_types():
    query = session.query(WorkType).all()
    return query

@router.post("", response_model=Union[createWorkTypeSchema, ErrorSchema])
async def create_work_type(workType: workTypeSchema):
    query = WorkType(name=workType.name, description=workType.description, default=workType.default)
    if session.query(WorkType).filter(WorkType.name == workType.name).all():
        return {"error": "Такой объект уже существует"}

    session.add(query)
    session.commit()

    return query



@router.get("/{workType_id}")
async def get_detail_work_type(workType_id: int):
    query = session.query(WorkType).get(workType_id)
    if query:
        return query
    return {"error": "Такой объект не найден"}

@router.delete("/{workType_id}")
async def delete_work_type(workType_id: int):
    query = session.query(WorkType).get(workType_id)
    if query:
        session.add(query)
        session.commit()
        return {"message": "deleted"}
    return {"error": "Такой объект не существует"}