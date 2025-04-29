from pydantic import BaseModel, EmailStr

# Incoming request body for register
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

# Incoming request body for login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Successful response for auth routes
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
