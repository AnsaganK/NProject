import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

DB_USER = "admin"
DB_PASSWORD = "4SvjIp54HhTN"
DB_HOST = "127.0.0.1"
DB_NAME = "navistar"

#DB_USER = "postgres"
#DB_PASSWORD = "12345"
#DB_HOST = "127.0.0.1"
#DB_NAME = "Navistar"

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)
engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_pre_ping=True, client_encoding='utf8'
)

Base = declarative_base()

