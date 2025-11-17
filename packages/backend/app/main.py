from fastapi import FastAPI

import app.api.v1.router as api_router

app = FastAPI()

app.include_router(api_router.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}