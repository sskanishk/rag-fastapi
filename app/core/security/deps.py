from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security.jwt import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_authenticated_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token missing subject (email)")
        return {"email": email}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
