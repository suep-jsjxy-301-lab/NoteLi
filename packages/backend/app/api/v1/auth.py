"""
app.api.v1.auth 的 Docstring
"""

from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    authenticate_user,
    validate_refresh_token,
)
from app.core.logger import logger
from app.models.models import User
from app.schemas.token import Token, RefreshToken, AccessToken
from app.schemas.user import UserOut
from app.schemas.response import ResponseModel
from app.utils.response import ok
# from app.core.config import cfg


auth_router = APIRouter(
    prefix="/auth",
    tags=["鉴权API"],
)


@auth_router.post(path="/token", response_model=ResponseModel[Token])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> ResponseModel[Token]:
    """
    用户登录并颁发 access_token + refresh_token。

    客户端需在表单中携带 username / password，成功后将得到双 token；
    access_token 默认有效期 15 分钟，refresh_token 7 天。
    后续可将 refresh_token 提交至 `/auth/refresh` 换取新的 access_token。

    Args:
        form_data: OAuth2 标准表单，FastAPI 自动注入。

    Returns:
        统一响应包装，data 字段为 Token 模型，含 access_token 与 refresh_token。

    Raises:
        HTTPException: 401 用户名或密码错误。

    Examples:
        ```bash
        curl -X POST https://api.example.com/auth/token \
             -d "username=alice&password=secret"
        ```
    """
    logger.debug(f"收到来自: {form_data.username}的登录请求")

    # 验证用户名密码
    user: User | Literal[False] = await authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成 access token 和 refresh token
    access_token: str = create_access_token(user=user)
    refresh_token: str = create_refresh_token(sub=user.id)
    # 可选：返回 refresh token，或单独在 /refresh 接口生成
    logger.info(f"{user.username} 登录成功")

    return ok(data=Token(access_token=access_token, refresh_token=refresh_token))


@auth_router.post(path="/tokenSwagger", response_model=Token)
async def login_for_access_token_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    专为 Swagger-UI 设计的登录接口，直接返回裸 Token 模型。

    业务逻辑与 `/auth/token` 完全一致，仅响应格式不同，方便前端在文档页面「Try it out」
    时无需解析统一包装层。

    Args:
        form_data: OAuth2 标准表单，FastAPI 自动注入。

    Returns:
        Token 模型，含 access_token 与 refresh_token。

    Raises:
        HTTPException: 401 用户名或密码错误。
    """
    logger.debug(f"收到来自: {form_data.username}的登录请求")

    # 验证用户名密码
    user: User | Literal[False] = await authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成 access token 和 refresh token
    access_token: str = create_access_token(user=user)
    refresh_token: str = create_refresh_token(sub=user.id)
    # 可选：返回 refresh token，或单独在 /refresh 接口生成
    logger.info(f"{user.username} 登录成功")

    return Token(access_token=access_token, refresh_token=refresh_token)


@auth_router.post(path="/refresh", response_model=ResponseModel[AccessToken])
async def refresh_access_token(req: RefreshToken) -> ResponseModel[AccessToken]:
    """
    凭借未过期的 refresh_token 换取新的 access_token。

    服务端会校验 refresh_token 的签名与过期时间，并提取用户身份；
    原 refresh_token 依旧有效，直到其自身过期。

    Args:
        req: 请求体，需携带 refresh_token。

    Returns:
        统一响应包装，data 字段为 AccessToken 模型，仅含新的 access_token。

    Raises:
        HTTPException: 401 refresh_token 无效或已过期。
    """
    current_user: User = await validate_refresh_token(refresh_token=req.refresh_token)
    new_access_token: str = create_access_token(user=current_user)
    return ok(data=AccessToken(access_token=new_access_token))


@auth_router.post(path="/logout")
async def logout(current_user: User = Depends(dependency=get_current_user)):
    """
    注销：通常需要将 token 加入黑名单（使用 Redis 等）
    这里简化返回成功。
    """
    # TODO: 将当前 token 的 jti 或 user_id + exp 加入 Redis 黑名单
    return {"msg": "Successfully logged out"}


@auth_router.get(path="/me", response_model=ResponseModel[UserOut])
async def read_users_me(
    current_user: User = Depends(dependency=get_current_user),
) -> ResponseModel[UserOut]:
    """
    获取当前登录用户的基本信息。

    Args:
        current_user: 由依赖注入的当前登录用户。

    Returns:
        统一响应包装，data 字段为 UserOut 模型（id、username、role）。
    """
    return ok(
        data=UserOut(
            id=current_user.id, username=current_user.username, role=current_user.role
        )
    )
