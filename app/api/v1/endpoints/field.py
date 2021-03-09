from . import session
from fastapi import APIRouter
from app.models.field import Field
from app.schemas.field import FieldSchema

router = APIRouter()


@router.get("/")
async def get_fields():
    query = session.query(Field).all()
    return query


@router.get("/{field_id}")
async def get_field(field_id: int):
    query = session.query(Field).filter(Field.id == field_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_field(field: FieldSchema):
    query = Field(name=field.name, kadastrNumber=field.kadastrNumber, coordinates=field.coordinates,
                  urlShpFile=field.urlShpFile, shapeArea=field.shapeArea, shapeLength=field.shapeLength,
                  districtId=field.districtId
                  )

    for i in session.query(Field).all():
        if i.kadastrNumber == field.kadastrNumber:
            return {"error": "A field with this kad.number has already been created"}

    session.add(query)
    session.commit()

    last_id = query.id
    organization = field.dict()

    return {**organization, "id": last_id}


@router.put("/{field_id}")
async def update_field(field_id:int, field: FieldSchema):
    query = session.query(Field).filter(Field.id == field_id).first()
    for i in session.query(Field).all():
        if i.kadastrNumber == Field.kadastrNumber and i.id != query.id:
            return {"error": "A field with this name has already been created"}
    if query:
        query.name = field.name
        query.kadastrNumber = field.kadastrNumber
        query.coordinates = field.coordinates
        query.urlShpFile = field.urlShpFile
        query.shapeArea = field.shapeArea
        query.shapeLength = field.shapeLength
        query.districtId = field.districtId
        return {"message": "Field ({}) updated".format(query.name)}
    return {"error": "Not Found"}

@router.delete("/{field_id}")
async def delete_field(field_id:int):
    query = session.query(Field).filter(Field.id == field_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Field ({}) deleted".format(query.name)}
    return {"error": "Not Found"}
