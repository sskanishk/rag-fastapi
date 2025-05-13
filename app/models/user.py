from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str
    password: str