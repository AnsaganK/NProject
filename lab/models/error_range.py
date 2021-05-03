from config import Base
from sqlalchemy import Table, Column, Integer, String, Float

'''
class ErrorRange(Base):
    __tablename__ = "errorRange"

    id = Column(Integer, primary_key=True)

    of = Column(Float)
    to = Column(Float)
    percent = Column(Float)

    def __repr__(self):
        return "<ErrorRange({})>".format(self.id)
'''