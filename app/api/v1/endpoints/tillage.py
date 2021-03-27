from db import session
from typing import Union
from fastapi import APIRouter
from app.schemas import ErrorSchema
from app.models.tillage import Tillage
from app.schemas.tillage import TillageSchema, CreateTillageSchema


router = APIRouter()

@router.get("")
async def get_tillages():
    query = session.query(Tillage).all()
    return query

@router.post("", response_model=CreateTillageSchema)
async def create_tillage(tillage: TillageSchema):
    query = Tillage(name=tillage.name, description=tillage.description)

    session.add(query)
    session.commit()

    return query

@router.get("/{tillage_id}")
async def get_tillage(tillage_id: int):
    query = session.query(Tillage).get(tillage_id)
    if query:
        return query
    return {"error": "Объект не найден"}

@router.delete("/{tillage_id}")
async def delete_tillage(tillage_id: int):
    query = session.query(Tillage).get(tillage_id)
    if query:
        session.delete(query)
        session.commit()
        return {"message": "deleted"}
    return {"error": "Объект не найден"}