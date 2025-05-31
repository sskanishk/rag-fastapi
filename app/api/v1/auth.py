from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import RegisterRequest, LoginRequest, TokenResponse
from app.models.response import SuccessResponse
from app.core.security.jwt import verify_password, create_access_token, create_refresh_token
from app.core.exceptions import APIException
from app.core.config import settings
from app.db.session import get_db
from app.services.user import create_user, get_user_by_email

ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
router = APIRouter()

@router.post("/register", response_model=SuccessResponse)
async def register_user(user: RegisterRequest, db: AsyncSession = Depends(get_db)):
    try:
        new_user = await create_user(db, user_data=user)
        return SuccessResponse(status=True, data={"email": new_user.email}, message="User registered successfully")
    except Exception as e:
        raise APIException(detail=str(e) or "Registration failed", status_code=500)

@router.post("/login", response_model=TokenResponse)
async def login_user(user: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        existing_user = await get_user_by_email(db, user.email)
        if not existing_user:
            raise APIException(detail="Invalid credentials", status_code=401)

        if not verify_password(user.password, existing_user.hashed_password):
            raise APIException(detail="Invalid credentials", status_code=401)
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        refresh_token = create_refresh_token(data={"sub": user.email})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=access_token_expires.total_seconds()
        )
    
    except APIException as exc:        
        raise APIException(detail=exc.detail, status_code=exc.status_code)
    
    except Exception as e:
        raise APIException(detail= str(e) or "Login failed", status_code=500)
