from pydantic import BaseModel, EmailStr, field_validator, Field

import re
from typing import Optional

# Incoming request body for register
class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str = Field(min_length=8, max_length=28)

    class Config:
        json_schema_extra = {
            'email': 'example@email.com',
            'password': 'Example@123!',
            'name': 'John Snow'
        }

    @field_validator('name')
    def validate_name(cls, value: str) -> str:
        if len(value) == 0 or value is None:
            raise ValueError("Name is requried")
        return value
    
    @field_validator('password')
    def validate_password_strength(cls, value: str) -> str:
        """
        Validate that the password meets complexity requirements.
        """
        if len(value) < 12:
            raise ValueError("Password must be at least 12 characters long")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[0-9]', value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("Password must contain at least one special character")
        if value.lower() == "password" or value.lower() == "password123":
            raise ValueError("That password is too common and insecure")
        return value

# Incoming request body for login
class LoginRequest(BaseModel):
    """
    User login request model with basic validation.
    """
    email: EmailStr = Field(..., description="The registered email address")
    password: str = Field(..., description="The user's password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123!"
            }
        }

# Successful response for auth routes
class TokenResponse(BaseModel):
    """
    Authentication token response model.
    """
    access_token: str = Field(
        ...,
        description="JWT access token for authenticated requests"
    )
    token_type: str = Field(
        default="bearer",
        description="Type of the returned token"
    )
    expires_in: Optional[int] = Field(
        default=None,
        description="Time in seconds until the token expires"
    )
    refresh_token: Optional[str] = Field(
        default=None,
        description="Token that can be used to obtain a new access token"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600,
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }