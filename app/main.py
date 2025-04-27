# app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging

# Setup logger
logger = setup_logging()

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

# print("settings",settings.APP_NAME)
# print("settings", settings.DEBUG)

@app.get("/xyz")
async def root():
    print("-----------------------------------------------Hello from root!")
    logger.info("Root endpoint accessed")
    return {"message": f"Welcome to {settings.APP_NAME}!"}
