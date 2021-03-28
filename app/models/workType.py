from config import Base
from sqlalchemy import Column, Integer, String, Boolean


class WorkType(Base):
    __tablename__ = "workType"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    default = Column(Boolean)
