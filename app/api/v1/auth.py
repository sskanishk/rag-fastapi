from fastapi import APIRouter, HTTPException
from app.models.auth_models import RegisterRequest, LoginRequest, TokenResponse
from app.models.response_models import SuccessResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.exceptions import APIException

router = APIRouter()

# In memory dummy "database"
dummy_user_db = {}

@router.post("/register", response_model=SuccessResponse)
async def register_user(user: RegisterRequest):
    try:
        if user.email in dummy_user_db:
            raise APIException(detail="User already exists", status_code=400)
        
        hashed_pwd = hash_password(user.password)
        dummy_user_db[user.email] = hashed_pwd
        
        return SuccessResponse(status=True, data={"email": user.email}, message="User registered successfully")
    except Exception as e:
        raise APIException(detail=str(e) or "Registration failed", status_code=500)

@router.post("/login", response_model=TokenResponse)
async def login_user(user: LoginRequest):
    try:
        if user.email not in dummy_user_db:
            raise APIException(detail="Invalid credentials", status_code=401)
        
        hashed_pwd = dummy_user_db[user.email]
        
        if not verify_password(user.password, hashed_pwd):
            raise APIException(detail="Invalid credentials", status_code=401)
        
        access_token = create_access_token(data={"sub": user.email})
        
        return TokenResponse(access_token=access_token)
    except Exception as e:
        raise APIException(detail= str(e) or "Login failed", status_code=500)
