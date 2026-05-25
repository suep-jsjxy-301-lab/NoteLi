import asyncio
from typing import Optional
from app.repositories import *
from app.models.models import User
from app.core.security import get_password_hash
from app.core.security import verify_password
from uuid import UUID


class UserService:
    @staticmethod
    async def authenticate(username: str, password: str) -> Optional[User]:
        user = await Repository.user.get_user_by_username(username)
        if user and verify_password(password, user.password):
            return user
        return None

    @staticmethod
    async def get_user_by_id(user_id: str | UUID) -> Optional[User]:
        """根据ID获取用户"""
        return await Repository.user.get_user_by_id(user_id)

    @staticmethod
    async def create_user(
        username: str, password: str, email: str, phone: str | None = None
    ) -> Optional[User]:
        """创建新用户服务"""
        if await Repository.user.get_user_by_username(username):
            return None
        if await Repository.user.get_user_by_email(email):
            return None
        if phone and await Repository.user.get_user_by_phone(phone):
            return None

        # 加密密码
        hashed_password = get_password_hash(password)

        # 创建用户
        user = await Repository.user.create_user(
            username=username, password=hashed_password, email=email, phone=phone
        )

        return user

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return await Repository.user.get_user_by_username(username)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return await Repository.user.get_user_by_email(email)

    @staticmethod
    async def get_user_by_phone(phone: str) -> Optional[User]:
        """根据手机号获取用户"""
        return await Repository.user.get_user_by_phone(phone)

    @staticmethod
    async def get_all_users() -> list[User]:
        """获取所有用户"""
        return await Repository.user.get_all_users()

    @staticmethod
    async def delete_user(user_id: UUID) -> bool:
        """删除用户"""
        return await Repository.user.delete_user(user_id)
    
    @staticmethod
    async def verify_password(username: str, password: str) -> bool:
        """验证用户密码"""
        user = await Repository.user.get_user_by_username(username)
        if not user:
            return False
        return verify_password(password, user.password)
    
    @staticmethod
    async def update_password(user_id: UUID, new_password: str) -> bool:
        """更新用户密码"""
        user = await Repository.user.get_user_by_id(user_id)
        if not user:
            return False
        hashed_password = get_password_hash(new_password)
        await Repository.user.change_password(user_id, hashed_password)
        return True
    
    @staticmethod
    async def update_email(user_id: UUID, new_email: str) -> bool:
        """更新用户邮箱"""
        user = await Repository.user.get_user_by_id(user_id)
        if not user:
            return False
        await Repository.user.change_email(user_id, new_email)
        return True
    
    @staticmethod
    async def update_phone(user_id: UUID, new_phone: Optional[str]) -> bool:
        """更新用户手机号"""
        user = await Repository.user.get_user_by_id(user_id)
        if not user:
            return False
        await Repository.user.change_phone(user_id, new_phone)
        return True
    
    @staticmethod
    async def update_username(user_id: UUID, new_username: str) -> bool:
        """更新用户名"""
        user = await Repository.user.get_user_by_id(user_id)
        if not user:
            return False
        await Repository.user.change_username(user_id, new_username)
        return True