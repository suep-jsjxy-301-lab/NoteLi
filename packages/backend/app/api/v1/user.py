# app/api/v1/user.py

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.response import ResponseModel
from app.schemas.user import UserIn, UserOut
from app.services.user import UserService
from app.utils.response import fail_conflict, ok, ok_created

user_router = APIRouter(
    prefix="/user",
    tags=["用户API"],
)


@user_router.post("/register", response_model=ResponseModel[UserOut])
async def register_user(payload: UserIn) -> ResponseModel[UserOut]:
    if await UserService.get_user_by_username(payload.username):
        return fail_conflict(message="用户名已存在")
    if await UserService.get_user_by_email(payload.email):
        return fail_conflict(message="邮箱已存在")
    if payload.phone and await UserService.get_user_by_phone(payload.phone):
        return fail_conflict(message="手机号已存在")

    user = await UserService.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        phone=payload.phone,
    )
    if user is None:
        return fail_conflict(message="用户注册失败")

    return ok_created(
        data=UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
        ),
        message="注册成功",
    )


@user_router.get("/me", response_model=ResponseModel[UserOut])
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> ResponseModel[UserOut]:
    return ok(
        data=UserOut(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            phone=current_user.phone,
        )
    )

