from fastapi import APIRouter
from app.models.response_models import SuccessResponse, ErrorResponse
from app.core.exceptions import APIException
from app.api.v1 import auth

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@router.get("/pingwithouterror", response_model=SuccessResponse)
async def ping():
    try:
        # Simulating normal working
        data = "pong"
        return SuccessResponse(status=True, data=data)
    except Exception as e:
        # Catching unexpected errors and raising properly
        print("excep ", e)
        raise APIException(detail = str(e) or "Failed to ping the service.", status_code = 500)
    
@router.get("/pingwitherror", response_model=SuccessResponse)
async def ping():
    try:
        # Force an exception (for testing)
        raise ValueError("Simulated error")
        # Simulating normal working
        
        data = "pong"
        return SuccessResponse(status=True, data=data)
    except Exception as e:
        # Catching unexpected errors and raising properly
        print("excep ", e)
        raise APIException(detail = str(e) or "Failed to ping the service.", status_code = 500)
