# app/main.py
from fastapi import FastAPI, logger
from app.core.logging import logger
from app.api.v1 import router

app = FastAPI()

app.include_router(router)
logger.info("服务启动")

@app.get("/")
async def root():
    return {"message": "Hello World"}
