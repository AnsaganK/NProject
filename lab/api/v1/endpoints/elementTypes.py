import time

from db import session
from fastapi import APIRouter
from lab.models.elements import ElementType, Type, Elements, Color, Range, RangeColor, ElementColor, ErrorRange, \
    ElementErrorRange
from sqlalchemy.orm import selectinload

from lab.schemas.elementTypes import elementTypeSchema
from lab.schemas.elements import ElementTypeSchema, ElementForTypeSchema

router = APIRouter()


@router.get("")
async def get_all_element_types():
    query = session.query(Type).options(selectinload(Type.elements)).all()
    return query


@router.get("/{type_id}")
async def get_all_element_types(type_id: int):
    query = session.query(Type).options(selectinload(Type.elements)).filter(Type.id == type_id).first()
    return query



@router.post("")
async def create_element_type(type: ElementTypeSchema):
    query = Type(name=type.name, gost=type.gost, description=type.description)

    session.add(query)
    session.commit()

    last_id = query.id
    query = session.query(Type).filter(Type.id == last_id).first()
    return query


@router.post("/add_element/{type_id}")
async def create_element_type(type_id: int, elements: ElementForTypeSchema):
    query = session.query(Type).filter(Type.id == type_id).first()
    for i in elements.elements:
        print(i)
        element = Elements(name=i.name, code=i.code, standard=i.standard, date=i.date)
        if not i.date:
            element.date = int(time.time())
        elementType = ElementType(element=element, type=query)
        for j in i.ranges:
            range_name = j.name
            range_of = j.of
            range_to = j.to
            range = Range(name=range_name, of=range_of, to=range_to)
            color = session.query(Color).filter(Color.id == j.color).first()
            if color:
                rangeColor = RangeColor(range=range, color=color)
                elementColor = ElementColor(elementType=elementType, rangeColor=rangeColor)
                session.add(elementColor)
        for k in i.errorRanges:
            rangeError = ErrorRange(of=k.of, to=k.to, value=k.value)
            elementErrorRange = ElementErrorRange(errorRange=rangeError, elementType=elementType)
            session.add(elementErrorRange)
    session.add(query)
    session.commit()

    last_id = query.id
    query = session.query(Type).filter(Type.id == last_id).first()
    return query


#@router.post("")
#async def create_element_types(type: elementTypeSchema):
#    query = Type(name= type.name)