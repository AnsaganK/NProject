from config import Base
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, JSON
from sqlalchemy.orm import relationship


class OrderPoints(Base):
    __tablename__ = "OrderPoints"

    id = Column(Integer, primary_key=True)
    orderId = Column(Integer, ForeignKey("orders.id"))
    order = relationship("Order", backref="points")
    orderGroupId = Column(Integer, ForeignKey("OrderGroup.id"))
    orderGroup = relationship("OrderGroup", backref="orders_points")
    dateCreate = Column(BigInteger)
    points = Column(JSON)

    def __repr__(self):
        return "<OrderPoints({})>".format(self.id)
