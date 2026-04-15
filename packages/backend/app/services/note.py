from typing import Optional

from app.models.models import Category, Note, User
from app.repositories import *


class NoteService:
    _DEFAULT_CATEGORY_NAME_BY_ID: dict[int, str] = {
        1: "全部笔记",
        2: "工作",
        3: "个人",
        4: "学习",
        5: "想法",
        6: "待办",
    }

    @classmethod
    def _resolve_category_name(
        cls, *, category: Optional[Category], category_id: int
    ) -> Optional[str]:
        if category is not None:
            return category.category_name
        return cls._DEFAULT_CATEGORY_NAME_BY_ID.get(category_id)

    @staticmethod
    async def create_note(
        *,
        user: User,
        category_id: int,
        title: str,
        content: str,
        tags: list[str],
        starred: bool,
    ) -> Note:
        category: Optional[Category] = await Category.filter(
            user=user, category_id=category_id
        ).first()
        category_name = NoteService._resolve_category_name(
            category=category, category_id=category_id
        )
        return await Repository.note.create_note(
            user=user,
            category=category,
            category_name=category_name,
            title=title,
            content=content,
            tags=tags,
            starred=starred,
        )

    @staticmethod
    async def update_note(
        *,
        user: User,
        note_id: int,
        category_id: int,
        title: str,
        content: str,
        tags: list[str],
        starred: bool,
    ) -> Note | None:
        note = await Repository.note.get_note_by_id(note_id)
        if note is None:
            return None
        if str(note.user_id) != str(user.id):
            return None

        category: Optional[Category] = await Category.filter(
            user=user, category_id=category_id
        ).first()
        category_name = NoteService._resolve_category_name(
            category=category, category_id=category_id
        )

        await Repository.note.save_note(
            note=note,
            category=category,
            category_name=category_name,
            title=title,
            content=content,
            tags=tags,
            starred=starred,
        )
        return await Repository.note.get_note_by_id(note_id)

    @staticmethod
    async def delete_note(*, user: User, note_id: int) -> bool:
        note = await Repository.note.get_note_by_id(note_id)
        if note is None:
            return False
        if str(note.user_id) != str(user.id):
            return False
        await Repository.note.delete_note(note)
        return True

    @staticmethod
    async def list_notes(*, user: User) -> list[Note]:
        return await Repository.note.get_notelist_by_user(user)
    
    @staticmethod
    async def get_note_by_id(*, user: User, note_id: int) -> Optional[Note]:
        note = await Repository.note.get_note_by_id(note_id)
        if note is None:
            return None
        if str(note.user_id) != str(user.id):
            return None
        return note
    
    @staticmethod
    async def update_note_starred( note: Note, starred: bool) -> bool:
        await Repository.note.update_note_starred(note=note, starred=starred)
        return True