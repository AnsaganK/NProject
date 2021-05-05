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
    query = Elements(name=type.name, gost=type.gost)

    session.add(query)
    session.commit()

    last_id = query.id
    return {"id": last_id}

#@router.post("")
#async def create_element_types(type: elementTypeSchema):
#    query = Type(name= type.name)