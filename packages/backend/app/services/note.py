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
        """创建笔记，自动解析分类名称"""
        category = await Repository.category.get_category_by_id(id=category_id)
        return await Repository.note.create_note(
            user=user,
            category=category,
            category_name=category.category_name,
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
        """更新笔记，自动解析分类名称"""
        note = await Repository.note.get_note_by_id(note_id)
        if note is None:
            return None
        if str(note.user_id) != str(user.id):
            return None

        category: Optional[Category] = await Repository.category.get_category_by_id(id=category_id)
        await Repository.note.save_note(
            note=note,
            category=category,
            category_name=category.category_name if category else NoteService._DEFAULT_CATEGORY_NAME_BY_ID.get(category_id),
            title=title,
            content=content,
            tags=tags,
            starred=starred,
        )
        return await Repository.note.get_note_by_id(note_id)

    @staticmethod
    async def delete_note(*, user: User, note_id: int) -> bool:
        """删除笔记，确保笔记存在且属于用户"""
        note = await Repository.note.get_note_by_id(note_id)
        if note is None:
            return False
        if str(note.user_id) != str(user.id):
            return False
        await Repository.note.delete_note(note)
        return True

    @staticmethod
    async def list_notes(*, user: User) -> list[Note]:
        """列出用户的所有笔记"""
        return await Repository.note.get_notelist_by_user(user)
    
    @staticmethod
    async def get_note_by_id(*, user: User, note_id: int) -> Optional[Note]:
        """根据笔记ID获取笔记，确保笔记存在且属于用户"""
        note = await Repository.note.get_note_by_id(note_id)
        if note is None:
            return None
        if str(note.user_id) != str(user.id):
            return None
        return note
    
    @staticmethod
    async def update_note_starred( note: Note, starred: bool) -> bool:
        """更新笔记的星标状态"""
        await Repository.note.update_note_starred(note=note, starred=starred)
        return True