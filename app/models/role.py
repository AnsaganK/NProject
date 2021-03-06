from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from config import Base
from app.models.RolePermission import RolesPermissions


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    title = Column(String)
    permissions = relationship("Permission", secondary=RolesPermissions, backref="roles")

    def __repr__(self):
        return "<Role ({})>".format(self.name)

