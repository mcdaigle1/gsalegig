from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from shared_utils.config_util import settings

engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()