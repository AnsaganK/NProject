from db import session
from fastapi import APIRouter, Query
from lab.models.elements import Color
from lab.schemas.elements import ColorSchema
import time

router = APIRouter()


@router.get("/")
async def get_elements():
    query = session.query(Color).all()
    return query


@router.get("/{color_id}")
async def get_element(color_id: int):
    query = session.query(Color).filter(Color.id == color_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_element(color: ColorSchema):
    query = Color(name=color.name, code=color.code)

    session.add(query)
    session.commit()

    last_id = query.id
    color = color.dict()
    return {**color, "id": last_id}

@router.put("/{color_id}")
async def update_color(color_id: int, color: ColorSchema):
    query = session.query(Color).filter(Color.id == color_id).first()
    if query:
        query.name = color.name
        query.code = color.code
        return {"message": "Color ({}) updated".format(query.name)}
    return {"error": "Not Found Color"}

@router.delete("/{color_id}")
async def delete_color(color_id: int):
    query = session.query(Color).filter(Color.id == color_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Color ({}) deleted".format(query.name)}
    return {"error": "Not Found Color"}