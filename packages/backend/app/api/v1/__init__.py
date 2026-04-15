# app/api/v1/__init__.py
from fastapi import APIRouter

import app.api.v1.chat as chat
import app.api.v1.auth as auth
import app.api.v1.user as user
import app.api.v1.category as category
import app.api.v1.note as note

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(chat.auth_router)
router.include_router(auth.auth_router)
router.include_router(user.user_router)
router.include_router(category.category_router)
router.include_router(note.note_router)

__all__: list[str] = ["router"]
