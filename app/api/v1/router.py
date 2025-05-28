from fastapi import APIRouter, Depends, Request
from app.models.response import SuccessResponse, ErrorResponse
from app.core.exceptions import APIException
from app.api.v1 import auth
from app.core.security.deps import get_authenticated_user
from app.core.rag.ingestion import start
from app.core.rag.generate import questionanswer
import json

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

@router.get("/me", response_model=SuccessResponse)
async def get_me(current_user: dict = Depends(get_authenticated_user)):
    try:
        return SuccessResponse(status=True, data={"user": current_user},message="You are authenticated")
    except Exception as e:
        print('exp ', str(e))
    raise APIException(detail = str(e) or "Failed to me the service.", status_code = 500)

@router.get("/rag", response_model=SuccessResponse)
async def rag():
    try:
        data = await start()
        return SuccessResponse(status=True, data=data)
    except Exception as e:
        raise APIException(detail = str(e) or "Failed to ping the service.", status_code = 500)
    
@router.get("/question", response_model=SuccessResponse)
async def question(request: Request):
    try:
        raw_body = await request.body()
        raw_json = raw_body.decode('utf-8')
        print("raw_body >>>> ", raw_json)
        try:
            prompt = json.loads(raw_json)
            print("Parsed prompt:", prompt)
        except json.JSONDecodeError:
            print("Invalid JSON received")
        data = await questionanswer(prompt)
        return SuccessResponse(status=True, data=data)
    except Exception as e:
        raise APIException(detail = str(e) or "Failed to ping the service.", status_code = 500)
