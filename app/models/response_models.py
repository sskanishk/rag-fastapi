from pydantic import BaseModel
from typing import Any, Optional

class SuccessResponse(BaseModel):
    status: bool
    data: Any
    message: Optional[str] = "Operation successful"

class ErrorResponse(BaseModel):
    status: bool
    message: str
    detail: Optional[str] = None
    error_code: Optional[int] = None
