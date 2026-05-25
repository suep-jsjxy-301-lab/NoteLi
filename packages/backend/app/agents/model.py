from uuid import UUID
from pydantic import BaseModel


class NoteModel(BaseModel):
    note_id: int
    user_id: UUID
    category_id: int
    title: str
    content: str
    tags: list[str]
    starred: bool

class CategoryModel(BaseModel):
    id : int
    category_id : int
    category_name : str