# app/api/v1/auth.py
"""
app.api.v1.auth 的 Docstring
"""

from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
    tags=["鉴权API"],
)


@auth_router.post("/token")
async def token():
    pass


@auth_router.post("/refresh")
async def refresh():
    pass


@auth_router.post("/logout")
async def logout():
    pass
