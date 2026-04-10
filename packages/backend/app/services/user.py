from typing import Optional
from app.repositories.user import UserRepository
from app.models.models import User
from app.core.security import get_password_hash
from app.core.security import verify_password
from uuid import UUID


class UserService:
    @staticmethod
    async def authenticate(username: str, password: str) -> User | None:
        user = await UserRepository.get_user_by_username(username)
        if user and verify_password(password, user.password):
            return user
        return None

    @staticmethod
    async def get_user_by_id(user_id: str | UUID) -> User | None:
        """根据ID获取用户"""
        return await UserRepository.get_user_by_id(user_id)

    @staticmethod
    async def create_user(
        username: str, password: str, email: str, phone: str | None = None
    ) -> Optional[User]:
        """创建新用户服务"""
        # 检查用户名是否已存在
        existing_user = await UserRepository.get_user_by_username(username)
        if existing_user:
            return None

        # 加密密码
        hashed_password = get_password_hash(password)

        # 创建用户
        user = await UserRepository.create_user(
            username=username, password=hashed_password, email=email, phone=phone
        )

        return user

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return await UserRepository.get_user_by_username(username)

    @staticmethod
    async def get_all_users() -> list[User]:
        """获取所有用户"""
        return await UserRepository.get_all_users()

    @staticmethod
    async def delete_user(user_id: UUID) -> bool:
        """删除用户"""
        return await UserRepository.delete_user(user_id)
