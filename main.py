from fastapi import FastAPI

from app.config import settings

app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.get("/")
async def root():
    return {"message": "Hello World"}
