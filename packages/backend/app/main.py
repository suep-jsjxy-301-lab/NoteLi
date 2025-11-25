# app/main.py
from fastapi import FastAPI

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


app.include_router(router)
logger.debug(f"Redis 配置: {cfg.redis.model_dump()}")


@app.get("/")
async def root():
    return {"message": "Hello World"}
