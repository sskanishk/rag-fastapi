from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt  # PyJWT

print("jwt path ------- ", jwt.__file__)  # Should show PyJWT's path
# from jwt import PyJWTError  # for error handling later if needed


# Load secret from env/config later, for now hardcoding
SECRET_KEY = "WWW.KANISHMALVIYA.XYZ"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire =  datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    print("herer ", to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
