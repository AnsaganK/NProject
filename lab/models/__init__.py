import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME


DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
)




#DATABASE_URL = "sqlite:///./test.db"
#DATABASE_URL = "postgresql://postgres:12345@127.0.0.1:5432/navia"

engine = sqlalchemy.create_engine(
    DATABASE_URL, pool_pre_ping=True, client_encoding='utf8'
)

Base = declarative_base()

