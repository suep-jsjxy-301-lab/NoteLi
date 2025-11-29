from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import jwt
from pwdlib import PasswordHash
from app.core.config import cfg

password_hash: PasswordHash = PasswordHash.recommended()

# ------ 配置 ------
SECRET_KEY: str = cfg.jwt.secret_key
ALGORITHM: str = cfg.jwt.algorithm


# ------ 纯算法 ------
def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(password=plain, hash=hashed)


def get_password_hash(password: str) -> str:
    return password_hash.hash(password=password)


def create_token(payload: Dict[str, Any], exp_delta: timedelta) -> str:
    to_encode: Dict[str, Any] = payload.copy()
    expire = int((datetime.now(tz=timezone.utc) + exp_delta).timestamp())
    to_encode.update({"exp": expire})
    return jwt.encode(payload=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)  # type: ignore


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
