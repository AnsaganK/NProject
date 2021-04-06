from app.models.cars import Car
from app.models.user import User
from db import session
from fastapi import APIRouter
from app.models.work import Work
from app.models.field import Field
from lab.models.mini_status import MiniStatus
from app.models.workType import WorkType
from app.models.workSubType import WorkSubType
from app.schemas.work import WorkSchema, createWorkSchema
from typing import Union
from app.schemas import ErrorSchema

router = APIRouter()

@router.get("")
async def get_works():
    query = session.query(Work).all()
    return query

@router.post("", response_model=Union[ErrorSchema, createWorkSchema])
async def create_works(work: WorkSchema):
    query = Work(name=work.name, description=work.description, geoJson=work.geoJson, startDate=work.startDate, endDate=work.endDate)

    field = session.query(Field).get(work.fieldId)
    if not field:
        return {"error": "Поле не найдено"}

    status = session.query(MiniStatus).get(work.statusId)
    if not status:
        return {"error": "Статус не найдено"}

    workType = session.query(WorkType).get(work.workTypeId)
    if not workType:
        return {"error": "Тип работы не найден"}

    workSubType = session.query(WorkSubType).get(work.workSubTypeId)
    if not workSubType:
        return {"error": "Подтип не найден"}

    if workSubType.groupId != workType.id:
        return {"error": "Данный подтип работы не относитя к нужному типу работы"}

    query.field = field
    query.status = status
    query.workType = workType
    query.workSubType = workSubType
    for c in work.cars:
        car = session.query(Car).filter(Car.id == c).first()
        organization = field.organization
        if car:
            if car.organization == organization:
                query.cars.append(car)
            else:
                return {"error":"У этой организации нет такого транспорта"}
    for u in work.users:
        user = session.query(User).filter(User.id == u).first()
        organization = field.organization
        if user:
            if user.organization == organization:
                query.users.append(user)
            else:
                return {"error":"У этой организации нет такого сотрудника"}
    session.add(query)
    session.commit()

    return query

@router.get("/{work_id}")
async def get_detail_work(work_id: int):
    query = session.query(Work).get(work_id)
    if query:
        return query
    return {"error": "Работа не найдена"}

@router.delete("/work_id")
async def delete_work(work_id: int):
    query = session.query(Work).get(work_id)
    if query:
        session.delete(query)
        session.commit()
        return {"message": "deleted"}
    return {"error": "Работа не найдена"}