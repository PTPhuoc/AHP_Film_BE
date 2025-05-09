from sqlalchemy import Column, Integer, Unicode, DateTime
from main.api.database import Base


class criteria_default(Base):
    __tablename__ = "criteriaDefault"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(Unicode(255), index=True, unique=True)