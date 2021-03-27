from db import session
from fastapi import APIRouter
from app.models.season import Season
from app.schemas import ErrorSchema
from app.schemas.season import SeasonSchema, CreateSeasonSchema
from typing import Union

router = APIRouter()


@router.get("")
async def get_seasons():
    query = session.query(Season).all()
    return query

@router.get("/{season_id}")
async def get_detail_season(season_id: int):
    query = session.query(Season).get(season_id)
    return query


@router.post("", response_model= Union[CreateSeasonSchema, ErrorSchema])
async def create_season(season: SeasonSchema):
    if session.query(Season).filter(Season.name == season.name).first():
        return {"error": "Объект с таким именем уже создан"}
    query = Season(name=season.name, of=season.of, to=season.to)

    session.add(query)
    session.commit()

    return query


@router.delete("/{season_id}")
async def delete_season(season_id: int):
    query = session.query(Season).get(season_id)
    if query:
        session.delete(query)
        session.commit()
        return {"message": "Season ({}) deleted".format(query.id)}
    return {"error": "Объект не найден"}
