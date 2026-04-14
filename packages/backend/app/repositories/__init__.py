# app/repositories/__init__.py
from .category import CategoryRepository
from .user import UserRepository

class Repository:
    category = CategoryRepository()
    user = UserRepository()

__all__: list[str] = ["Repository"]