from db import session
from typing import Union
from fastapi import APIRouter
from app.schemas import ErrorSchema
from app.models.field import Field
from app.models.culture import Culture
from app.models.season import Season
from app.models.irrigationType import IrrigationType
from app.models.tillage import Tillage
from app.models.fieldCultureSeason import FieldCultureSeason
from app.schemas.fieldCultureSeason import FieldCultureSeasonSchema, CreateFieldCultureSeasonSchema
from sqlalchemy.orm import selectinload

router = APIRouter()

@router.get("")
async def get_field_culture_season():
    query = session.query(FieldCultureSeason).all()
    return query


@router.post("", response_model=Union[ErrorSchema, CreateFieldCultureSeasonSchema])
async def create_field_culture_season(fcs: FieldCultureSeasonSchema):
    if session.query(FieldCultureSeason).filter(FieldCultureSeason.fieldId == fcs.fieldId,
                                                FieldCultureSeason.cultureId == fcs.cultureId,
                                                FieldCultureSeason.seasonId == fcs.seasonId).first():
        return {"error": "Для данного поля уже есть такие данные"}

    field = session.query(Field).get(fcs.fieldId)
    if not field:
        return {"error": "Объект поля не существует"}

    culture = session.query(Culture).get(fcs.cultureId)
    if not culture:
        return {"error": "Объект культуры не существует"}

    season = session.query(Season).get(fcs.seasonId)
    if not season:
        return {"error": "Объект сезона не существует"}

    irrigationType = session.query(IrrigationType).get(fcs.irrigationTypeId)
    if not irrigationType:
        return {"error": "Объект тип орошения не существует"}

    tillage = session.query(Tillage).get(fcs.tillageId)
    if not tillage:
        return {"error": "Объект обработки почвы не существует"}

    sort = fcs.sort
    FCS = FieldCultureSeason(field=field, culture=culture, season=season,
                             tillage=tillage, irrigationType=irrigationType, sort=sort,
                             sowingDate=fcs.sowingDate, cleaningDate=fcs.cleaningDate,
                             prolificness=fcs.prolificness, harvest=fcs.harvest
                             )

    session.add(FCS)
    session.commit()

    return FCS

@router.get("/{field_id}")
async def get_crop_rotation_for_field(field_id: int):
    field = session.query(Field).get(field_id)
    query = session.query(FieldCultureSeason).options(selectinload(FieldCultureSeason.culture)).options(selectinload(FieldCultureSeason.season)).options(selectinload(FieldCultureSeason.irrigationType)).options(selectinload(FieldCultureSeason.tillage)).filter(FieldCultureSeason.fieldId == field_id).all()
    return {"field":field, "cropRotations": query}

#@router.get("/{field_id}")
#async def get_field_culture_season(field_id: int):
#    query =