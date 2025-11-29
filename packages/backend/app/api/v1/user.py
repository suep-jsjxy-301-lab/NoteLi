# app/api/v1/user.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Any


from app.models.models import User
from app.schemas.user import UserOut, UserIn
from app.services.user import UserService
from app.utils.response import ok, ok_created, fail_conflict, fail_forbidden

user_router = APIRouter(
    prefix="/user",
    tags=["用户API"],
)

