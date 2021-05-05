from db import session
from fastapi import APIRouter
from lab.models.elements import ElementType, Type, Elements
from sqlalchemy.orm import selectinload

from lab.schemas.elementTypes import elementTypeSchema
from lab.schemas.elements import ElementTypeSchema

router = APIRouter()


@router.get("")
async def get_all_element_types():
    query = session.query(Type).options(selectinload(Type.element)).all()
    return query


@router.post("/create_element_type")
async def create_element_type(type: ElementTypeSchema):
    query = Type(name=type.name, gost=type.gost, description=type.description)

    session.add(query)
    session.commit()

    last_id = query.id
    query = session.query(Type).filter(Type.id == last_id).first()
    return {**query}

#@router.post("")
#async def create_element_types(type: elementTypeSchema):
#    query = Type(name= type.name)