# app/main.py

from fastapi import FastAPI, HTTPException
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exception_handler import api_exception_handler, http_exception_handler
from app.core.exceptions import APIException

# Setup logger
logger = setup_logging()

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# print("settings",settings.APP_NAME)
# print("settings", settings.DEBUG)

# Register exception handlers globally
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

@app.get("/xyz")
async def root():
    print("-----------------------------------------------Hello from root!")
    logger.info("Root endpoint accessed")
    return {"message": f"Welcome to {settings.APP_NAME}!"}

@app.get("/error")
async def trigger_error():
    # This is to manually trigger an error for testing
    raise APIException("Something went wrong!", status_code=500)
