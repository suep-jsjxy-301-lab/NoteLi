from typing import Optional
from app.models.models import User
from uuid import UUID


class UserRepository:
    @staticmethod
    async def create_user(
        username: str, password: str, email: str, phone: str | None = None
    ) -> User:
        """创建新用户"""
        user = await User.create(
            username=username, password=password, email=email, phone=phone
        )
        return user

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        """根据用户名获取用户"""
        user = await User.filter(username=username).first()
        return user

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        user = await User.filter(email=email).first()
        return user

    @staticmethod
    async def get_user_by_phone(phone: str) -> Optional[User]:
        """根据手机号获取用户"""
        user = await User.filter(phone=phone).first()
        return user

    @staticmethod
    async def get_user_by_id(user_id:  str | UUID) -> Optional[User]:
        """根据ID获取用户"""
        user = await User.filter(id=user_id).first()
        return user

    @staticmethod
    async def get_all_users() -> list[User]:
        """获取所有用户"""
        users = await User.all()
        return users

    @staticmethod
    async def delete_user(user_id: UUID) -> bool:
        """删除用户"""
        deleted_count = await User.filter(id=user_id).delete()
        return deleted_count > 0
    
    @staticmethod
    async def change_password(user_id: UUID, new_hashed_password: str) -> bool:
        """修改用户密码"""
        updated_count = await User.filter(id=user_id).update(password=new_hashed_password)
        return updated_count > 0
    
    @staticmethod
    async def change_email(user_id: UUID, new_email: str) -> bool:
        """修改用户邮箱"""
        updated_count = await User.filter(id=user_id).update(email=new_email)
        return updated_count > 0
    
    @staticmethod
    async def change_phone(user_id: UUID, new_phone: Optional[str]) -> bool:
        """修改用户手机号"""
        updated_count = await User.filter(id=user_id).update(phone=new_phone)
        return updated_count > 0
