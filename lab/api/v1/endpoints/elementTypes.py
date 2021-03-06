import time

from db import session
from fastapi import APIRouter
from lab.models.element_type import ElementType
from lab.models.elements import Type, Elements, Color, Range, RangeColor, ElementColor, ErrorRange, \
    ElementErrorRange
from sqlalchemy.orm import selectinload

from lab.schemas.elementTypes import elementTypeSchema
from lab.schemas.elements import ElementTypeSchema, ElementForTypeSchema

router = APIRouter()


@router.get("")
async def get_all_element_types():
    query = session.query(Type).options(selectinload(Type.elements)).all()
    response = []
    for i in query:
        dic = {}
        dic["name"] = i.name
        dic["description"] = i.description
        dic["gost"] = i.gost
        dic["id"] = i.id
        dic["elements"] = []
        for j in i.elements:
            if j.element:
                elementName = j.element.name
                elementCode = j.element.code
                dic["elements"].append({"elementName": elementName,
                                        "elementCode": elementCode,
                                        "elementId": j.element.id,
                                        "typeId": j.type.id,
                                        "id": j.id,
                                        })
        response.append(dic)
    return response

def wrap_element_type(data):
    dic = {**data.__dict__}
    elements = []
    for i in data.elements:
        colorRangesList = []
        errorRanges = session.query(ErrorRange).join(ElementErrorRange).filter(ElementErrorRange.elementTypeId == i.id).all()
        colorRanges = session.query(RangeColor).join(ElementColor).filter(ElementColor.elementTypeId == i.id).all()

        for j in colorRanges:
            colorRangesList.append({
                "color": j.color,
                "range": j.range
            })
        element = session.query(Elements).filter(Elements.id == i.elementId).first()
        if element:
            elements.append({
                "errorRanges": errorRanges,
                "colorRanges": colorRangesList,
                "element": element,
            })
    dic["elements"] = elements
    return dic


@router.get("/{type_id}")
async def get_all_element_types(type_id: int):
    query = session.query(Type).options(selectinload(Type.elements)).filter(Type.id == type_id).first()
    if query:
        return wrap_element_type(query)
    return {"error": "?????? ???? ????????????"}


@router.post("")
async def create_element_type(type: ElementTypeSchema):
    query = Type(name=type.name, gost=type.gost, description=type.description)

    session.add(query)
    session.commit()

    last_id = query.id
    query = session.query(Type).filter(Type.id == last_id).first()
    return query

@router.delete("/{type_id}")
async def delete_element_type(type_id: int):
    query = session.query(Type).filter(Type.id == type_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "???????????? ?????? ????????????"}
    return {"error": "???????????? ???? ????????????"}

@router.post("/add_element/{type_id}")
async def create_element_type(type_id: int, elements: ElementForTypeSchema):
    query = session.query(Type).filter(Type.id == type_id).first()
    query.name = elements.name
    query.description = elements.description
    query.gost = elements.gost
    data = []
    newEls = []
    #query.elements = []
    oldEls = [i.elementId for i in query.elements]
    for i in elements.elements:
        if i.elementId not in oldEls:
            newEls.append(i)

    for i in query.elements:
        for el in elements.elements:
            print(i.elementId, " == ", el.elementId)
            if i.elementId == el.elementId:
                data.append(i)
                elementType = session.query(ElementType).filter(ElementType.elementId == i.elementId).filter(ElementType.typeId == query.id).first()
                elementType.color = []
                elementType.element_types = []
                session.add(elementType)
                session.commit()
                for j in el.colorRanges:
                    range_name = j.name
                    range_of = j.of
                    range_to = j.to
                    range = Range(name=range_name, of=range_of, to=range_to)
                    color = session.query(Color).filter(Color.id == j.color).first()
                    if color:
                        rangeColor = RangeColor(range=range, color=color)
                        elementColor = ElementColor(elementType=elementType, rangeColor=rangeColor)
                        session.add(elementColor)
                for k in el.errorRanges:
                    rangeError = ErrorRange(of=k.of, to=k.to, value=k.value)
                    if rangeError:
                        elementErrorRange = ElementErrorRange(errorRange=rangeError, elementType=elementType)
                        session.add(elementErrorRange)


    #query.elements = []
    #query.elements = data
    print()
    print(query.elements)
    print()
    for i in newEls:
        print(i)
        element = session.query(Elements).filter(Elements.id == i.elementId).first()
        elementType = ElementType(element=element, type=query)
        for j in i.colorRanges:
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
            if rangeError:
                elementErrorRange = ElementErrorRange(errorRange=rangeError, elementType=elementType)
                session.add(elementErrorRange)
    session.add(query)
    session.commit()

    last_id = query.id
    query = session.query(Type).options(selectinload(Type.elements)).filter(Type.id == last_id).first()
    return wrap_element_type(query)


