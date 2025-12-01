# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logger import logger
from app.api.v1 import router
from app.core.config import cfg
from app.core.lifespan import lifespan
from app.core.errors import register_exception_handlers


from app.middleware import RequestTimerMiddleware

app = FastAPI(lifespan=lifespan)
register_exception_handlers(app=app)

# app.add_middleware(middleware_class=Always200Middleware)
app.add_middleware(middleware_class=RequestTimerMiddleware)

origins = [
    "https://localhost",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
logger.debug(f"Redis 配置: {cfg.redis.model_dump()}")


@app.get("/")
async def root():
    return {"message": "Hello World"}
