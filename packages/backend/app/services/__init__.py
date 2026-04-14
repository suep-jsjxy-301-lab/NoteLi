# app/services/__init__.py
from .category import CategoryService
from .user import UserService
from .token import TokenService

class Service:
    category = CategoryService()
    user = UserService()
    token = TokenService()

__all__: list[str] = ["Service"]