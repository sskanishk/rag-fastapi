# app/main.py

from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

print("settings",settings.APP_NAME)
print("settings", settings.DEBUG)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.APP_NAME}!"}
