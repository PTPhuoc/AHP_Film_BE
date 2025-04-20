from sqlalchemy import Column, Integer, String, Unicode, ForeignKey
from main.api.database import Base
from sqlalchemy.orm import relationship


class Criterias(Base):
    __tablename__ = "Criterias"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    caculatorId = Column(String(255), ForeignKey("Caculators.id"), index=True)
    name = Column(Unicode(255), index=True)
    index = Column(Integer, index=True)

    caculator = relationship("Caculators", back_populates="criteria")
