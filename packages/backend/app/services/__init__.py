# app/services/__init__.py
from .category import CategoryService
from .user import UserService
from .token import TokenService
from .note import NoteService

class Service:
    category = CategoryService()
    user = UserService()
    token = TokenService()
    note = NoteService()

__all__: list[str] = ["Service"]