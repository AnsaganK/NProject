import os

import json
from typing import List

from fastapi.params import Depends
import shutil
import shapefile as shp
import zipfile

#from pytz import unicode
from fastapi.responses import FileResponse
from app.auth.auth_bearer import JWTBearer
from app.models.historyFields import HistoryFields
from app.models.shape import Shape
from app.models.user import User
from app.views.auth.auth_bearer import decodeJWT
from db import session
from fastapi import APIRouter, File, UploadFile
from app.models.field import Field
from app.models.typesForField import TypesForField
from app.schemas.field import FieldSchema
from .organization import Organization
from app.schemas.organization import OrganizationSchema
import time

from sqlalchemy.orm import selectinload


router = APIRouter()

@router.get("")
async def get_fields():
    #query = session.query(Field, Organization.id).join(Field.organization).all()
    #query = session.query(Field.name, Field.organization.label('organization')).all()
    query = session.query(Field).options(selectinload(Field.organization)).options(selectinload(Field.type)).all()
    return query

def createShape(geometry, kadNumber):
    url = 'shapefile/{}'.format(kadNumber)
    w = shp.Writer(url)
    w.field('name', 'C')
    w.poly(geometry)
    w.record('{}'.format(kadNumber))
    w.close()
    z = zipfile.ZipFile('media/edit_shape_zip/{}.zip'.format(kadNumber), 'w')
    files = [url+'.shx', url+'.shp', url+'.dbf']
    for file in files:
        z.write(file)
    z.close()

def createGeoJson(urlShape):
    s = shp.Reader(urlShape)
    fields = s.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in s.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature",
                            geometry=geom, properties=atr))

        # write the GeoJSON file
    return {"type": "FeatureCollection", "features": buffer}



@router.post("/shape_to_geojson")
async def shape_to_geojson(shape: List[UploadFile] = File(...)):
    now = time.time()*1000
    url = "media/shape/{0}".format(str(int(now)))
    for i in shape:
        urlShape = "media/shape/{0}.{1}".format(str(int(now)), i.filename[-3:])
        with open(urlShape, "wb") as f:
            shutil.copyfileobj(i.file, f)
    geoJson = createGeoJson(url)
    query = Shape(date=int(now), geoJson=geoJson, url=url)
    session.add(query)
    session.commit()

    last_query = session.query(Shape).filter(Shape.id == query.id).first()
    return last_query



@router.get("/history/{field_id}")
async def get_history_for_field(field_id: int):
    query = session.query(HistoryFields).options(selectinload(HistoryFields.user)).filter(HistoryFields.fieldId == field_id).all()
    return query


@router.get("/organization/{organization_id}")
async def get_field(organization_id: int):
    #query = session.query(Organization).options(selectinload(Organization.fields)).filter(Organization.id == organization_id).all()
    query = session.query(Field).join(Organization).options(selectinload(Field.type)).filter(Organization.id == organization_id).all()
    if query:
        return query
    return {"error": "Not Found"}


@router.get("/download/{field_id}")
async def download_field_geojson(field_id: int):
    query = session.query(Field).filter(Field.id == field_id).first()
    json = query.geoJson
    kadNumber = query.kadNumber
    createShape(json["geometry"]["coordinates"], kadNumber)
    return FileResponse("media/edit_shape_zip/{}.zip".format(kadNumber))


    
@router.get("/{field_id}")
async def get_field(field_id: int):
    query = session.query(Field).options(selectinload(Field.type)).options(selectinload(Field.shape)).filter(Field.id == field_id).first()
    #print(query.__dict__)
    if query:
        a = query.organization
        return query.__dict__
    return {"error": "Not Found"}



@router.post("")
async def create_field(field: FieldSchema, token: str = Depends(JWTBearer())):
    user = decodeJWT(token)
    user = session.query(User).filter(User.id == user["id"]).first()
    #print("userId: ", user)
    query = Field(name=field.name, kadNumber=field.kadNumber,
                  urlShpFile=field.urlShpFile,
                  districtId=field.districtId,
                  geoJson=field.geoJson, length=field.length, area=field.area
                  )

    organization = session.query(Organization).filter(Organization.id == field.organizationId).first()
    type = session.query(TypesForField).filter(TypesForField.id == field.typeId).first()
    shape = session.query(Shape).filter(Shape.id == field.shapeId).first()
    if not organization:
        return {"error": "Not Found Organization"}
    if not type:
        return {"error": "Not Found Type"}
    for i in session.query(Field).all():
        if i.kadNumber == field.kadNumber:
            return {"error": "A field with this kad.number has already been created"}

    query.organization = organization
    query.type = type
    if shape:
        query.shape = shape
    history = HistoryFields(field=query, user=user, date=int(time.time()), action="Создано", geoJson=field.geoJson)
    session.add(query)
    session.add(history)
    session.commit()

    last_id = query.id
    organization = field.dict()

    return {**organization, "id": last_id}


@router.get("/shapes/{shape_id}")
async def download_shape(shape_id: int):
    shape = session.query(Shape).filter(Shape.id == shape_id).first()
    files = [shape.url+".shp", shape.url+".dbf"]
    #print(files)
    z = zipfile.ZipFile("{}.zip".format(shape.url.replace("shape", "zip")), 'w')
    for file in files:
        z.write(file)
    z.close()
    file_name = "{}.zip".format(shape.url.replace("shape", "zip"))
    return FileResponse(file_name)

@router.put("/{field_id}")
async def update_field(field_id:int, field: FieldSchema, token: str = Depends(JWTBearer())):
    user = decodeJWT(token)
    user = session.query(User).filter(User.id == user["id"]).first()
    query = session.query(Field).filter(Field.id == field_id).first()
    for i in session.query(Field).all():
        if i.kadNumber == field.kadNumber and i.id != query.id:
            return {"error": "A field with this name has already been created"}
    organization = query.organization
    type = session.query(TypesForField).filter(TypesForField.id == field.typeId).first()
    if query:
        query.name = field.name
        query.kadNumber = field.kadNumber
        query.urlShpFile = field.urlShpFile
        query.districtId = field.districtId
        query.organization = organization
        query.geoJson = field.geoJson
        query.length = field.length
        query.area = field.area
        query.type = type
        history = HistoryFields(field=query, user=user, date=int(time.time()), action="Изменено", geoJson=field.geoJson)
        session.add(query)
        session.add(history)
        session.commit()
        print(query.type)
        print(query.organization)
        return {**query.__dict__}
    return {"error": "Not Found"}

@router.delete("/{field_id}")
async def delete_field(field_id:int):
    query = session.query(Field).filter(Field.id == field_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Field ({}) deleted".format(query.name)}
    return {"error": "Not Found"}

@router.get("/geojson/{field_id}")
async def get_geojson_for_field(field_id: int):
    field = session.query(Field).get(field_id)
    featureCollection = {"type": "FeatureCollection", "features":[]}
    featureCollection["features"].append(field.geoJson)
    return featureCollection