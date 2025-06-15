from pydantic import BaseModel
from typing import Any, Optional, List

class SuccessResponse(BaseModel):
    status: bool
    data: Any
    message: Optional[str] = "Operation successful"

class CachedSource(BaseModel):
    question: str
    response: str
    similarity: float

class AnswerContent(BaseModel):
    answer: str
    sources: List[CachedSource]

class ErrorResponse(BaseModel):
    status: bool
    message: str
    detail: Optional[str] = None
    error_code: Optional[int] = None
