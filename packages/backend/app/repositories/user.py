from typing import Optional
from app.models.models import User
from uuid import UUID


class UserRepository:
    @staticmethod
    async def create_user(username: str, password: str, role: str = "user") -> User:
        """创建新用户"""
        user = await User.create(username=username, password=password, role=role)
        return user

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """根据用户名获取用户"""
        user = await User.filter(username=username).first()
        return user

    @staticmethod
    async def get_user_by_id(user_id: UUID) -> Optional[User]:
        """根据ID获取用户"""
        user = await User.filter(id=user_id).first()
        return user

    @staticmethod
    async def get_all_users() -> list[User]:
        """获取所有用户"""
        users = await User.all()
        return users

    @staticmethod
    async def update_user_role(user_id: UUID, role: str) -> bool:
        """更新用户角色"""
        updated_count = await User.filter(id=user_id).update(role=role)
        return updated_count > 0

    @staticmethod
    async def delete_user(user_id: UUID) -> bool:
        """删除用户"""
        deleted_count = await User.filter(id=user_id).delete()
        return deleted_count > 0
