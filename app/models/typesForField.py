from config import Base
from sqlalchemy import Column, Integer, String


class TypesForField(Base):
    __tablename__ = "TypesForField"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    key = Column(String)

    def __repr__(self):
        return "<fieldTypes ({})>".format(self.name)