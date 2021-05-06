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

def wrap_element_type(data):
    dic = {**data.__dict__}
    elements = []
    for i in data.elements:
        errorRange = session.query(ElementErrorRange).filter(ElementErrorRange.elementTypeId == i.id).first()
        element = session.query(Elements).filter(Elements.id == i.elementId).first()
        elements.append({
            "errorRange": errorRange,
            "element": element,
        })
    dic["elements"] = elements
    return dic


@router.get("/{type_id}")
async def get_all_element_types(type_id: int):
    query = session.query(Type).options(selectinload(Type.elements)).filter(Type.id == type_id).first()
    if query:
        return wrap_element_type(query)
    return {"error": "Тип не найден"}


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
        element = session.query(Elements).filter(Elements.id == i.elementId).first()
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
    query = session.query(Type).options(selectinload(Type.elements)).filter(Type.id == last_id).first()
    return query


#@router.post("")
#async def create_element_types(type: elementTypeSchema):
#    query = Type(name= type.name)