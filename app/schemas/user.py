from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    name: str

# Properties to receive on user creation
class UserCreate(UserBase):
    pass

# Properties to return to client
class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
