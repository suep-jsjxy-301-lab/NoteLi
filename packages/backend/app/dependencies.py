"""
FastAPI 依赖函数集合
所有“从 token 到 User”的函数全放这里，供 router 层复用。
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.services.user import UserService
from app.models.models import User  # 仅用于类型注解，运行时不会循环

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/tokenSwagger")


async def get_current_user(
    token: Annotated[str, Depends(dependency=oauth2_scheme)],
) -> User:
    """
    验证 Bearer token，返回当前登录用户。
    如果 token 无效或用户不存在，抛 401。
    """
    from app.core.security import decode_token  # 延迟导入避免循环

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="验证密钥失败",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="验证密钥失败",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserService.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="验证密钥失败",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """可扩展：检查用户是否激活/被禁用"""
    return current_user


async def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """确保当前用户是管理员，否则抛 403"""
    if current_user.username != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只有管理员可以执行此操作",
        )
    return current_user

