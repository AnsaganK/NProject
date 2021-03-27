from sqlalchemy import Column, Integer, String
from config import Base


class Tillage(Base):
    __tablename__ = "tillages"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __repr__(self):
        return "<tillage ({})>".format(self.name)