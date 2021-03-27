from typing import Union
from db import session
from fastapi import APIRouter
from app.schemas import ErrorSchema
from app.models.culture import Culture
from app.schemas.culture import CultureSchema, CreateCultureSchema

router = APIRouter()

@router.get("")
async def get_cultures():
    query = session.query(Culture).all()
    return query


@router.get("/{culture_id}")
async def get_detail_culture(culture_id: int):
    query = session.query(Culture).get(culture_id)
    return query


@router.post("", response_model= Union[CreateCultureSchema, ErrorSchema])
async def create_culture(culture: CultureSchema):
    if session.query(Culture).filter(Culture.name == culture.name).first():
        return {"error": "Объект с таким именем уже создан"}
    query = Culture(name=culture.name, default=culture.default, shortName=culture.shortName, description=culture.description, fillColor=culture.fillColor)

    session.add(query)
    session.commit()

    return query


@router.delete("/{culture_id}")
async def delete_culture(culture_id: int):
    query = session.query(Culture).get(culture_id)
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Culture ({}) deleted".format(query.id)}
    return {"error": "Объект не найден"}
