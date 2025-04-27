# app/core/exception_handler.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import APIException
from app.core.logging import setup_logging

logger = setup_logging()

# Global exception handler
async def api_exception_handler(request: Request, exc: APIException):
    logger.error(f"Error occurred during request to {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Handle HTTPException (FastAPI default exception)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error occurred during request to {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

