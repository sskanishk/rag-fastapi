import uuid
from sqlalchemy import Column, Text, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from app.db.base import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    question_embedding = Column(Vector, nullable=False)
    response = Column(Text, nullable=False)
    response_embedding = Column(Vector, nullable=False)
    is_helpful = Column(Boolean)
    created_by = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
