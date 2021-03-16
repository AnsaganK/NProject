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
