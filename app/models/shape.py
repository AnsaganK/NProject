from config import Base
from sqlalchemy import Table, String, Integer, Column, JSON, BigInteger


class Shape(Base):
    __tablename__ = "shapes"

    id = Column(Integer, primary_key=True)
    geoJson = Column(JSON)
    url = Column(String)
    date = Column(BigInteger)

    def __repr__(self):
        return "".format(self.id, self.url)