from . import session
from fastapi import APIRouter, Depends
from lab.models.samples import Samples
from lab.schemas.samples import SamplesSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from fastapi.security import HTTPBearer
import time

from app.models.organization import Organization
from lab.models.elements import Elements

router = APIRouter()


@router.get("/")
async def get_samples():
    query = session.query(Samples).all()
    for i in query:
        a = i.elements
        b = i.client
    return query


@router.get("/{element_id}")
async def get_sample(element_id: int):
    query = session.query(Samples).filter(Samples.id == element_id).first()
    if query:
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_sample(sample: SamplesSchema):
    date = sample.date
    if not date:
        date = int(time.time())

    sampleQuery = Samples(amount=sample.amount, date=date)
    for i in sample.elements:
        element = session.query(Elements).filter(Elements.id == int(i)).first()
        if element:
            sampleQuery.elements.append(element)

    for i in sample.client:
        client = session.query(Organization).filter(Organization.id == int(i)).first()
        if client:
            sampleQuery.client.append(client)
    session.add(sampleQuery)
    session.commit()
    return {**sample.dict(), "id": sampleQuery.id}
    #query = Samples(client=sample.client, amount=sample.amount, elements=sample.elements)





'''
@router.put("/{sample_id}")
async def update_sample(sample_id: int, sample: SamplesSchema):
    query = session.query(Samples).filter(Samples.id == sample_id).first()
    
    if query:
        query.name = element.name
        query.code = element.code
        query.date = element.date

        return {"message": "Element ({}) updated".format(query.name)}
    return {"error": "Not Found"}
'''

@router.delete("/{sample_id}")
async def delete_organization(sample_id: int):
    query = session.query(Samples).filter(Samples.id == sample_id).first()
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Sample ({}) deleted".format(query.id)}
    return {"error": "Not Found"}