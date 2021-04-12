from sqlalchemy.orm import selectinload

from db import session
from fastapi import APIRouter, Query
from lab.models.elements import Elements, Type, ElementType, Range, Color, RangeColor, ElementColor
from lab.schemas.elements import ElementsSchema
import time

router = APIRouter()


def wrap_type_element(query):
    if query:
        dic = {"id": query.id, "name": query.name, "code": query.code, "date": query.date, "types": []}
        types = query.types
        for type in types:
            t = {"name": type.type.name, "range": []}
            element_type = session.query(ElementType).filter(ElementType.element == query).filter(
                ElementType.type == type).first()
            element_colors = session.query(ElementColor).filter(ElementColor.elementType == element_type).all()
            for j in element_colors:
                range_color = j.rangeColor
                r = {"name": range_color.range.name, "of": range_color.range.of, "to": range_color.range.to,
                     "color": range_color.color.id, "code": range_color.color.code}
                t["range"].append(r)
            dic["types"].append(t)
        return dic

    return None


@router.get("")
async def get_elements(*, main: bool = Query(False)):
    query = session.query(Elements).all()
    data = []
    for i in query:
        a = wrap_type_element(i)
        if a:
            data.append(a)
    if main:
        query = session.query(Elements).filter(Elements.standard == True).all()
        for i in query:
            a = wrap_type_element(i)
            if a:
                data.append(a)
    return data


@router.get("/{element_id}")
async def get_element(element_id: int):
    query = session.query(Elements).filter(Elements.id == element_id).first()
    a = wrap_type_element(query)
    if a:
        return a
    else:
        return {"error": "Элемент не найден"}


@router.post("/")
async def create_element(element: ElementsSchema):
    query = Elements(name=element.name, code=element.code, standard=element.standard, date=element.date)
    if not query.date:
        query.date = int(time.time())
    for i in session.query(Elements).all():
        if i.name == element.name:
            return {"error": "A element with this name has already been created"}

    for i in element.types:
        type = Type(name=i.name)
        elementType = ElementType(type=type, element=query)
        for j in i.range:
            range_name = j.name
            range_of = j.of
            range_to = j.to
            range = Range(name=range_name, of=range_of, to=range_to)
            color = session.query(Color).filter(Color.id == j.color).first()
            if color:
                rangeColor = RangeColor(range=range, color=color)
                elementColor = ElementColor(elementType=elementType, rangeColor=rangeColor)
                session.add(elementColor)
    session.add(query)
    session.commit()

    last_id = query.id
    organization = element.dict()

    return {**organization, "id": last_id}


@router.put("/{element_id}")
async def update_element(element_id: int, element: ElementsSchema):
    query = session.query(Elements).filter(Elements.id == element_id).first()
    for i in session.query(Elements).all():
        if i.name == element.name and i.id != query.id:
            return {"error": "A element with this name has already been created"}
    if query:
        query.name = element.name
        query.code = element.code
        query.standard = element.standard
        if element.date:
            query.date = element.date
        else:
            query.date = int(time.time())

        for i in query.types:
            type = i
            session.delete(type)
            for j in session.query(ElementColor).filter(ElementColor.elementType == type).all():
                session.delete(j)
        session.commit()
        for i in element.types:
            type = Type(name=i.name)
            elementType = ElementType(type=type, element=query)
            for j in i.range:
                range_name = j.name
                range_of = j.of
                range_to = j.to
                range = Range(name=range_name, of=range_of, to=range_to)
                color = session.query(Color).filter(Color.id == j.color).first()
                if color:
                    rangeColor = RangeColor(range=range, color=color)
                    elementColor = ElementColor(elementType=elementType, rangeColor=rangeColor)
                    session.add(elementColor)
        session.commit()
        dic = {"name": query.name, "code": query.code, "date": query.date, "types": []}
        types = query.types
        for type in types:
            t = {"name": type.type.name, "range": []}
            element_type = session.query(ElementType).filter(ElementType.element == query).filter(
                ElementType.type == type).first()
            element_colors = session.query(ElementColor).filter(ElementColor.elementType == element_type).all()
            for j in element_colors:
                range_color = j.rangeColor
                r = {"name": range_color.range.name, "of": range_color.range.of, "to": range_color.range.to,
                     "color": range_color.color.id}
                t["range"].append(r)
            dic["types"].append(t)
        return dic
    return {"error": "Not Found"}


@router.delete("/{element_id}")
async def delete_element(element_id: int):
    query = session.query(Elements).filter(Elements.id == element_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Element ({}) deleted".format(query.name)}
    return {"error": "Not Found"}
