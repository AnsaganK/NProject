from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

DB_USER = "postgres"
DB_PASSWORD = "12345"
DB_HOST = "127.0.0.1"
DB_NAME = "Navistar"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
engine = sqlalchemy.create_engine(
    DATABASE_URL
)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
