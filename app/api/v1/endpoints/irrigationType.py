from db import session
from typing import Union
from fastapi import APIRouter
from app.schemas import ErrorSchema
from app.models.irrigationType import IrrigationType
from app.schemas.irrigationType import IrrigationTypeSchema, CreateIrrigationTypeSchema


router = APIRouter()

@router.get("")
async def get_irrigation_types():
    query = session.query(IrrigationType).all()
    return query

@router.post("", response_model=CreateIrrigationTypeSchema)
async def create_irrigation_type(irrigationType: IrrigationTypeSchema):
    query = IrrigationType(name=irrigationType.name, description=irrigationType.description)

    session.add(query)
    session.commit()

    return query

@router.get("/{irrigationType_id}")
async def get_irrigation_types(irrigationType_id: int):
    query = session.query(IrrigationType).get(irrigationType_id)
    if query:
        return query
    return {"error": "Объект не найден"}

@router.delete("/{irrigationType_id}")
async def delete_irrihation_type(irrigationType_id: int):
    query = session.query(IrrigationType).get(irrigationType_id)
    if query:
        session.delete(query)
        session.commit()
        return {"message": "deleted"}
    return {"error": "Объект не найден"}