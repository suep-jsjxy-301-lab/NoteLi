# app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Literal, cast, Dict
from copy import deepcopy

from uuid import UUID
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import cfg
from app.schemas.token import TokenData
from app.models.models import User


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY: str = cfg.jwt.secret_key
ALGORITHM: str = cfg.jwt.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES: int = cfg.jwt.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS: int = cfg.jwt.refresh_token_expire_days

password_hash: PasswordHash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/tokenSwagger")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(password=plain_password, hash=hashed_password)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password=password)


async def get_user(username: str) -> User | None:
    user: User | None = await User.filter(username=username).first()
    return user


async def authenticate_user(username: str, password: str) -> User | Literal[False]:
    user: User | None = await get_user(username=username)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user


# 用3.9+内置的dict支持泛型
def create_token(
    payload: dict[str, Any], expires_delta: timedelta | None = None
) -> str:  # Changed return type from bytes to str
    to_encode: dict[str, Any] = deepcopy(x=payload)
    if expires_delta:
        expire: datetime = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt  # type: ignore


def create_access_token(user: User, expires_delta: timedelta | None = None) -> str:
    scope: Literal["admin", "user"] = cast(Literal["admin", "user"], user.role)

    iat: datetime = datetime.now(timezone.utc)
    exp: datetime = iat + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    data: dict[str, Any] = TokenData(
        sub=str(object=user.id),  # Convert UUID to string for JSON serialization
        iat=iat,
        exp=exp,
        username=user.username,
        scope=scope,
    ).model_dump()

    return create_token(payload=data)  # Return the string directly


def create_refresh_token(sub: UUID | str) -> str:
    expire: datetime = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    data: dict[str, Any] = {
        "sub": str(object=sub) if isinstance(sub, UUID) else sub,
        "iat": datetime.now(tz=timezone.utc),
        "exp": expire,
        "type": "refresh",
    }
    return create_token(payload=data)  # Return the string directly


async def get_current_user(
    token: Annotated[str, Depends(dependency=oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict[str, Any] = jwt.decode(
            jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: Any | None = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(**payload)
    except InvalidTokenError:
        raise credentials_exception
    user: User | None = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: User = Depends(dependency=get_current_user),
) -> User:
    # 可以在这里添加用户是否激活的检查
    return current_user


async def get_admin_user(current_user: User = Depends(dependency=get_current_user)):
    """获取当前管理员用户，如果不是管理员则抛出403异常"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只有管理员可以执行此操作",
        )
    return current_user


async def validate_refresh_token(refresh_token: str) -> User:
    """
    校验 refresh_token：
      1. 解码并验签
      2. 必须带 type == "refresh"
      3. sub 字段必须是已注册用户
    返回对应的 User 对象，方便后续重新签发 access_token。
    """
    exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: Dict[str, Any] = jwt.decode(
            jwt=refresh_token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except InvalidTokenError:
        raise exc

    if payload.get("type") != "refresh":
        raise exc

    user_id: Any | None = payload.get("sub")
    if not user_id:
        raise exc

    user: User | None = await User.filter(id=user_id).first()
    if not user:
        raise exc

    return user
