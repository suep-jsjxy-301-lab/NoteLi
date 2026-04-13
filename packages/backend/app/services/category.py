from typing import Optional
from app.repositories.user import CategoryRepository
from app.models.models import Category
from uuid import UUID

class CategoryService:
    @staticmethod
    async def create_category(user_id: UUID, category_id: int, category_name: str) -> Optional[Category]:
        """创建新分类服务"""
        if await CategoryRepository.get_category_by_user_and_category_name(user_id, category_name):
            return None

        category = await CategoryRepository.create_category(
            user_id=user_id, category_id=category_id, category_name=category_name
        )

        return category

    @staticmethod
    async def get_categories_by_user_id(user_id: UUID) -> list[Category]:
        """根据用户ID获取分类列表"""
        return await CategoryRepository.get_categories_by_user_id(user_id)

    @staticmethod
    async def delete_category(id: int) -> bool:
        """删除分类"""
        category = await CategoryRepository.get_category_by_id(id)
        if not category:
            return False
        await CategoryRepository.delete_category(id)
        return True
    
    @staticmethod
    async def update_category(id: int, new_category_name: str) -> bool:
        """更新分类名称"""
        category = await CategoryRepository.get_category_by_id(id)
        if not category:
            return False
        await CategoryRepository.update_category_name(id, new_category_name)
        return True
    
    @staticmethod
    async def get_category_by_user_and_category_name(user_id: UUID, category_name: str) -> Optional[Category]:
        """根据用户ID和分类名称获取分类"""
        return await CategoryRepository.get_category_by_user_and_category_name(user_id, category_name)

    @staticmethod
    async def delete_categories_by_user_id(user_id: UUID) -> None:
        """根据用户ID删除所有分类"""
        await CategoryRepository.delete_categories_by_user_id(user_id)