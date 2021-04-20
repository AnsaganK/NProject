from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
engine = sqlalchemy.create_engine(
    DATABASE_URL, client_encoding='utf8'
)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
