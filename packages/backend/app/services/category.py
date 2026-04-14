from typing import Optional
from app.repositories import *
from app.models.models import Category, User
from app.schemas.category import CategoryOut

class CategoryService:
    @staticmethod
    async def create_category(user: User, category_id: int, category_name: str) -> Optional[Category]:
        """创建新分类服务"""
        if await Repository.category.get_category_by_user_and_category_name(user, category_name):
            return None

        category = await Repository.category.create_category(
            user=user, category_id=category_id, category_name=category_name
        )

        return category

    @staticmethod
    async def get_categories_by_user(user: User) -> list[Category]:
        """根据用户获取分类列表"""
        return await Repository.category.get_categories_by_user_id(user)

    @staticmethod
    async def delete_category(id: int) -> bool:
        """删除分类"""
        category = await Repository.category.get_category_by_id(id)
        if not category:
            return False
        await Repository.category.delete_category(id)
        return True
    
    @staticmethod
    async def update_category(id: int, new_category_id: int, new_category_name: str) -> CategoryOut:
        """更新分类"""
        isUpdate = await Repository.category.update_category(
            id=id, new_category_id=new_category_id, new_category_name=new_category_name
        )
        if not isUpdate:
            return None
        category = await Repository.category.get_category_by_id(id)
        return CategoryOut(
            id=category.id,
            category_id=category.category_id,
            category_name=category.category_name,
        )
    
    @staticmethod
    async def get_category_by_user_and_category_name(user: User, category_name: str) -> Optional[Category]:
        """根据用户和分类名称获取分类"""
        return await Repository.category.get_category_by_user_and_category_name(user, category_name)

    @staticmethod
    async def delete_categories_by_user_id(user: User) -> None:
        """根据用户删除所有分类"""
        await Repository.category.delete_categories_by_user_id(user)

    @staticmethod
    async def get_category_by_id(id: int) -> Optional[Category]:
        """根据分类ID获取分类"""
        return await Repository.category.get_category_by_id(id)