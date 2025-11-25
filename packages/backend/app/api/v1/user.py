# app/api/v1/user.py

from fastapi import APIRouter, Depends, HTTPException
from typing import Any

from app.core.security import get_admin_user
from app.models.models import User
from app.schemas.user import UserOut, UserIn
from app.services.user import UserService
from app.utils.response import ok, ok_created, fail_conflict, fail_forbidden

user_router = APIRouter(
    prefix="/user",
    tags=["用户API"],
)


@user_router.post("/create", response_model=UserOut)
async def create_user(
    user_in: UserIn, 
    current_user: User = Depends(get_admin_user)
):
    """
    创建新用户
    只有管理员可以创建用户
    """
    # 确保不接受已加密的密码，只接受明文密码
    user = await UserService.create_user(
        username=user_in.username, 
        password=user_in.password, 
        role=getattr(user_in, 'role', 'user')  # 如果没有指定角色，默认为'user'
    )
    
    if user is None:
        # 用户名已存在
        raise HTTPException(
            status_code=409,
            detail="用户名已存在"
        )
    
    # 使用UserOut模型返回用户信息（不包含密码）
    user_out = UserOut.from_tortoise_orm(user)
    return ok_created(data=user_out, message="用户创建成功")


@user_router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: str, 
    current_user: User = Depends(get_admin_user)
):
    """
    获取用户信息
    只有管理员可以查看用户信息
    """
    from uuid import UUID
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="无效的用户ID格式"
        )
    
    user = await UserService.get_user_by_id(user_uuid)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在"
        )
    
    user_out = UserOut.from_tortoise_orm(user)
    return ok(data=user_out)


@user_router.get("/", response_model=list[UserOut])
async def list_users(
    current_user: User = Depends(get_admin_user)
):
    """
    获取所有用户列表
    只有管理员可以查看用户列表
    """
    users = await UserService.get_all_users()
    users_out = [UserOut.from_tortoise_orm(user) for user in users]
    return ok(data=users_out)
