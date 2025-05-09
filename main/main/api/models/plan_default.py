from sqlalchemy import Column, Integer, Unicode, Float
from main.api.database import Base
from sqlalchemy.orm import relationship


class PlanDefault(Base):
    __tablename__ = "planDefault"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(Unicode(255), index=True, unique=True)
    category = Column(Unicode(255), index=True)
    imdb = Column(Float, index=True)
    duration = Column(Float, index=True)
    director = Column(Unicode(255), index=True)
    awards = Column(Unicode(255), index=True)
    nation = Column(Unicode(255), index=True)

    plans = relationship("Plans", back_populates="plan_default", cascade="all, delete-orphan")
