from config import Base
from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Boolean, Table
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy import ForeignKey


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    role_edit_id = Column(Integer, ForeignKey("roles.id"))
    role_edit = relationship("Role", backref="status_edit", foreign_keys=[role_edit_id])

    role_selection_id = Column(Integer, ForeignKey("roles.id"))
    role_selection = relationship("Role", backref="status_selection", foreign_keys=[role_selection_id])

    color = Column(String)

    def __repr__(self):
        return self.name
