from typing import Optional
from app.repositories.user import UserRepository
from app.models.models import User
from app.core.security import get_password_hash
from uuid import UUID


class UserService:
    @staticmethod
    async def create_user(username: str, password: str, role: str = "user") -> Optional[User]:
        """创建新用户服务
        
        Args:
            username: 用户名
            password: 密码（明文，会在服务层加密）
            role: 用户角色，默认为"user"
            
        Returns:
            User: 创建成功的用户对象，如果用户名已存在则返回None
        """
        # 检查用户名是否已存在
        existing_user = await UserRepository.get_user_by_username(username)
        if existing_user:
            return None
        
        # 加密密码
        hashed_password = get_password_hash(password)
        
        # 创建用户
        user = await UserRepository.create_user(
            username=username, 
            password=hashed_password, 
            role=role
        )
        
        return user

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return await UserRepository.get_user_by_username(username)

    @staticmethod
    async def get_user_by_id(user_id: UUID) -> Optional[User]:
        """根据ID获取用户"""
        return await UserRepository.get_user_by_id(user_id)

    @staticmethod
    async def get_all_users() -> list[User]:
        """获取所有用户"""
        return await UserRepository.get_all_users()

    @staticmethod
    async def update_user_role(user_id: UUID, role: str) -> bool:
        """更新用户角色"""
        return await UserRepository.update_user_role(user_id, role)

    @staticmethod
    async def delete_user(user_id: UUID) -> bool:
        """删除用户"""
        return await UserRepository.delete_user(user_id)
