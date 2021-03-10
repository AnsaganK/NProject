from . import session
from fastapi import APIRouter, Depends
from lab.models.selection import Selection
from lab.schemas.selection import SelectionSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT
from fastapi.security import HTTPBearer
import time
from app.models.organization import Organization
from .samples import Samples

router = APIRouter()


@router.get("/")
async def get_selection():
    query = session.query(Selection).all()
    for i in query:
        a = i.organization
        b = i.samples
    return query


@router.get("/{element_id}")
async def get_element(element_id: int):
    query = session.query(Selection).filter(Selection.id == element_id).first()
    if query:
        a = query.organization
        b = query.samples
        return query
    return {"error": "Not Found"}


@router.post("/")
async def create_selection(selection: SelectionSchema):
    organization = session.query(Organization).filter(Organization.id == selection.organization).first()
    if not organization:
        return {"error": "Not Found Organization"}
    samples = session.query(Samples).join(Samples.client).filter(Samples.id == selection.samples, Organization.id == organization.id).first()
    if not samples:
        return {"error": "Not Found Samples"}
    print(organization)
    amount = 0
    for i in samples.selection:
        amount += i.amount
    if selection.amount > samples.amount - amount or selection.amount > samples.amount:
        return {"error": "amount<{}".format(samples.amount-amount)}
    query = Selection(amount=selection.amount, status=selection.status, date=selection.date)
    query.organization.append(organization)
    query.samples.append(samples)
    if not query.date:
        query.date = time.time()
    session.add(query)
    session.commit()

    last_id = query.id
    selection = selection.dict()

    return {**selection, "id": last_id}

