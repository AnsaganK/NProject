from db import session
from fastapi import APIRouter
from app.models.field import Field
from app.models.typesForField import TypesForField
from app.schemas.field import FieldSchema
from .organization import Organization
from app.schemas.organization import OrganizationSchema

from sqlalchemy.orm import selectinload


router = APIRouter()


@router.get("/")
async def get_fields():
    #query = session.query(Field, Organization.id).join(Field.organization).all()
    #query = session.query(Field.name, Field.organization.label('organization')).all()
    query = session.query(Field).options(selectinload(Field.organization)).options(selectinload(Field.type)).all()
    return query


@router.get("/{field_id}")
async def get_field(field_id: int):
    query = session.query(Field).filter(Field.id == field_id).first()
    print(query.__dict__)
    if query:
        a = query.organization
        return query.__dict__
    return {"error": "Not Found"}

@router.get("/organization/{organization_id}")
async def get_field(organization_id: int):
    #query = session.query(Organization).options(selectinload(Organization.fields)).filter(Organization.id == organization_id).all()
    query = session.query(Field).join(Organization).filter(Organization.id == organization_id).all()
    if query:
        return query
    return {"error": "Not Found"}

@router.post("/")
async def create_field(field: FieldSchema):
    query = Field(name=field.name, kadNumber=field.kadNumber,
                  urlShpFile=field.urlShpFile,
                  districtId=field.districtId,
                  geoJson=field.geoJson, length=field.length, area=field.area
                  )

    organization = session.query(Organization).filter(Organization.id == field.organizationId).first()
    type = session.query(TypesForField).filter(TypesForField.id == field.typeId).first()
    if not organization:
        return {"error": "Not Found Organization"}
    if not type:
        return {"error": "Not Found Type"}
    for i in session.query(Field).all():
        if i.kadNumber == field.kadNumber:
            return {"error": "A field with this kad.number has already been created"}


    query.organization = organization
    query.type = type

    session.add(query)
    session.commit()

    last_id = query.id
    organization = field.dict()

    return {**organization, "id": last_id}


@router.put("/{field_id}")
async def update_field(field_id:int, field: FieldSchema):
    query = session.query(Field).filter(Field.id == field_id).first()
    for i in session.query(Field).all():
        if i.kadastrNumber == Field.kadNumber and i.id != query.id:
            return {"error": "A field with this name has already been created"}
    if query:
        query.name = field.name
        query.kadastrNumber = field.kadNumber
        query.urlShpFile = field.urlShpFile
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
