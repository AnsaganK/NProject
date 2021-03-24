from db import session
from fastapi import APIRouter
from lab.models.elements import ElementType, Type, Elements
from sqlalchemy.orm import selectinload

router = APIRouter()


@router.get("/")
async def get_all_element_types():
    query = session.query(Type).options(selectinload(Type.element)).all()
    return query