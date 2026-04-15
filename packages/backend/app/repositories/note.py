from typing import Optional

from app.models.models import Category, Note, User


class NoteRepository:
    @staticmethod
    async def get_note_by_id(note_id: int) -> Optional[Note]:
        return await Note.filter(id=note_id).first()

    @staticmethod
    async def create_note(
        *,
        user: User,
        category: Optional[Category],
        category_name: Optional[str],
        title: str,
        content: str,
        tags: list[str],
        starred: bool,
    ) -> Note:
        return await Note.create(
            user=user,
            category=category,
            category_name=category_name,
            title=title,
            content=content,
            tags=tags,
            starred=starred,
        )

    @staticmethod
    async def save_note(
        *,
        note: Note,
        category: Optional[Category],
        category_name: Optional[str],
        title: str,
        content: str,
        tags: list[str],
        starred: bool,
    ) -> Note:
        note.category = category
        note.category_name = category_name
        note.title = title
        note.content = content
        note.tags = tags
        note.starred = starred
        await note.save()
        return note

    @staticmethod
    async def delete_note(note: Note) -> None:
        await note.delete()

    @staticmethod
    async def get_notelist_by_user(user: User) -> list[Note]:
        return await Note.filter(user=user).all()
