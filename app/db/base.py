# from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# make sure models get loaded as soon as you import Base
from app.db.models import Document