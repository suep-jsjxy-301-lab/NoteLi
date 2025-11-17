from fastapi import APIRouter

import app.api.v1.chat as chat

router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)

router.include_router(chat.router)