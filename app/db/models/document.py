import uuid
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID
# from pgvector.sqlalchemy import Vector
from app.db.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    # embedding = Column(Vector(1536), nullable=False)
