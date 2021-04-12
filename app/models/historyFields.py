from sqlalchemy.orm import relationship

from config import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger


class HistoryFields(Base):
    __tablename__ = "HistoryFields"

    id = Column(Integer, primary_key=True)

    fieldId = Column(Integer, ForeignKey('fields.id'))
    field = relationship('Field', backref="history")

    userId = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="history")

    action = Column(String)

    date = Column(Integer)

    def __repr__(self):
        return "<HistoryField ({})>".format(self.id)


