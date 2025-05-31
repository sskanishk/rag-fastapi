# app/main.py

from fastapi import FastAPI, HTTPException
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exception_handler import api_exception_handler, http_exception_handler
from app.core.exceptions import APIException
from app.models.response import SuccessResponse, ErrorResponse
from app.api.v1.router import router as v1_router

print("App Name:", settings.APP_NAME)
print("Debug mode:", settings.DEBUG)

# Setup logger
logger = setup_logging()

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# Register exception handlers globally
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(v1_router, prefix="/api/v1")

@app.get("/", response_model=SuccessResponse)
async def root():
    # This is for testing root route
    logger.info("Root endpoint accessed")
    return SuccessResponse(status=True, data=f"Welcome to {settings.APP_NAME}!")

@app.get("/error", response_model=ErrorResponse)
async def trigger_error():
    # This is to manually trigger an error for testing
    raise APIException("Something went wrong!", status_code=500)
