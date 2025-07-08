from fastapi import APIRouter, Depends, Request
from app.models.response import SuccessResponse, ErrorResponse
from app.core.exceptions import APIException
from app.api.v1 import auth
from app.core.security.deps import get_authenticated_user
from app.rag import ingestion
from app.rag import generate
from app.rag import mark_response
import json

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@router.get("/ingest", response_model=SuccessResponse)
async def ingest(current_user: dict = Depends(get_authenticated_user)):
    try:
        data = await ingestion.main()
        return SuccessResponse(status=True, data=data)
    except Exception as e:
        raise APIException(detail = str(e) or "Failed to ping the service.", status_code = 500)
    
@router.get("/ask", response_model=SuccessResponse)
async def ask(request: Request, current_user: dict = Depends(get_authenticated_user)):
    try:
        raw_body = await request.body()
        raw_json = raw_body.decode('utf-8')
        try:
            prompt = json.loads(raw_json)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON received")
        data = await generate.main(prompt)
        return SuccessResponse(status=True, data=data)
    except Exception as e:
        raise APIException(detail = str(e) or "Failed to ping the service.", status_code = 500)
    
@router.get("/mark_response", response_model=SuccessResponse)
async def ask(request: Request, current_user: dict = Depends(get_authenticated_user)):
    try:
        raw_body = await request.body()
        raw_json = raw_body.decode('utf-8')
        try:
            payload = json.loads(raw_json)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON received")
        data = await mark_response.main(payload)
        return SuccessResponse(status=True, data=data)
    except Exception as e:
        raise APIException(detail = str(e) or "Failed to ping the service.", status_code = 500)
