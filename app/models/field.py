from app.models import Base
from sqlalchemy import Column, Integer, String

class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    kadastrNumber = Column(String, unique=True)
    coordinates = Column(String)
    urlShpFile = Column(String)
    shapeArea = Column(String)
    shapeLength = Column(String)
    districtId = Column(String)

    def __repr__(self):
        return "<Field ({})>".format(self.kadastr)
