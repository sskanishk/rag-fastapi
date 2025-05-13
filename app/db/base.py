# # from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# # make sure models get loaded as soon as you import Base
# # from app.db.models.document_model import Document
# # from app.db.models.user_model import User

# # below snippet requires when to run init_db.py
# # from .models import (
# #     User,
# #     Document
# # )

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all database models."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate __tablename__ automatically from the class name."""
        return cls.__name__.lower()


# Optional: If you need to enforce a naming convention
# from sqlalchemy import MetaData
# metadata = MetaData(naming_convention={
#     "ix": "ix_%(column_0_label)s",
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(constraint_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s"
# })
# Base.metadata = metadata