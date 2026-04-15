# app/repositories/__init__.py
from .category import CategoryRepository
from .user import UserRepository
from .note import NoteRepository

class Repository:
    category = CategoryRepository()
    user = UserRepository()
    note = NoteRepository()

__all__: list[str] = ["Repository"]