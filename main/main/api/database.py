from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from django.conf import settings

# Tạo engine
engine = create_engine(settings.DATABASE_URL)

# Tạo Session
SessionLocal = sessionmaker(bind=engine)

# Base class cho model
Base = declarative_base()

from .models import Caculators, Criterias, Plans, pair_of_criterias, pair_of_plans

Base.metadata.create_all(bind=engine)