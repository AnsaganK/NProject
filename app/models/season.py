from sqlalchemy import Column, String, Integer, BigInteger
from config import Base


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    of = Column(BigInteger)
    to = Column(BigInteger)



    def __repr__(self):
        return "<season ({})>".format(self.name)