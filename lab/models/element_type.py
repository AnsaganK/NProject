from sqlalchemy import Column, Integer, String
from config import Base
from sqlalchemy.orm import relationship

from sqlalchemy import ForeignKey
from lab.models.order import OrderGroupElementsType, OrderElementsType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .elements import Elements

class ElementType(Base):
    __tablename__ = "ElementType"

    id = Column(Integer, primary_key=True)
    typeId = Column(Integer, ForeignKey('types.id'))
    type = relationship("Type", cascade="all,delete", backref="elements")
    elementId = Column(Integer, ForeignKey('elements.id'))
    element = relationship("Elements",  backref="types")

    orderGroups = relationship("OrderGroup", secondary=OrderGroupElementsType, back_populates="elementTypes")
    orders = relationship("Order", secondary=OrderElementsType, back_populates="elementTypes")

    def __repr__(self):
        return "<ElementType ({})>".format(self.id)