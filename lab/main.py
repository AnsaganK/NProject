from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from lab.core.config import settings
from lab.api.v1.api import api_router
import sqlalchemy
from app.models import Base, DATABASE_URL, engine
from app.main import metadata
import sys

sys.setrecursionlimit(1500000)
app = FastAPI(title="KazAgroLab",
              version="1.0.0",
              openapi_url=f"{settings.API_V1_STR}/openapi.json"
              )

app.include_router(api_router, prefix=settings.API_V1_STR)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)