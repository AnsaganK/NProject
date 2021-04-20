from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.api import api_router as app_router
from lab.api.v1.api import api_router as lab_router

import sqlalchemy
from config import Base, DATABASE_URL, engine

app = FastAPI(title="Navia",
              version="1.0.0",
              openapi_url=f"{settings.API_V1_STR}/openapi.json"
              )

app.include_router(lab_router, prefix=settings.API_V1_STR)
#app.include_router(app_router, prefix=settings.API_V1_STR)

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metadata = sqlalchemy.MetaData(DATABASE_URL)
Base.metadata.create_all(engine)
