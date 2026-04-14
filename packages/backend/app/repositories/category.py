from typing import Optional
from app.models.models import Category, User

class CategoryRepository:
    @staticmethod
    async def create_category(user: User, category_id: int, category_name: str) -> Category:
        """创建新分类"""
        category = await Category.create(user=user, category_id=category_id, category_name=category_name)
        return category

    @staticmethod
    async def get_categories_by_user_id(user: User) -> list[Category]:
        """根据用户获取分类列表"""
        categories = await Category.filter(user=user).all()
        return categories

    @staticmethod
    async def delete_category(id: int) -> bool:
        """删除分类"""
        deleted_count = await Category.filter(id=id).delete()
        return deleted_count > 0
    
    @staticmethod
    async def update_category_name(id: int, new_category_name: str) -> bool:
        """更新分类名称"""
        updated_count = await Category.filter(id=id).update(category_name=new_category_name)
        return updated_count > 0
    
    @staticmethod
    async def get_category_by_user_and_category_name(user: User, category_name: str) -> Optional[Category]:
        """根据用户和分类名称获取分类"""
        category = await Category.filter(user=user, category_name=category_name).first()
        return category
    
    @staticmethod
    async def get_category_by_id(id: int) -> Optional[Category]:
        """根据分类ID获取分类"""
        category = await Category.filter(id=id).first()
        return category
    
    @staticmethod
    async def delete_categories_by_user_id(user: User) -> None:
        """根据用户删除所有分类"""
        await Category.filter(user=user).delete()

    @staticmethod
    async def update_category_id(id: int, new_category_id: int) -> bool:
        """更新分类ID"""
        updated_count = await Category.filter(id=id).update(category_id=new_category_id)
        return updated_count > 0
    
    @staticmethod
    async def update_category_name(id: int, new_category_name: str) -> bool:
        """更新分类名称"""
        updated_count = await Category.filter(id=id).update(category_name=new_category_name)
        return updated_count > 0
    
    @staticmethod
    async def update_category(id: int, new_category_id: int, new_category_name: str) -> bool:
        """更新分类"""
        updated_count = await Category.filter(id=id).update(
            category_id=new_category_id,
            category_name=new_category_name
        )
        return updated_count > 0