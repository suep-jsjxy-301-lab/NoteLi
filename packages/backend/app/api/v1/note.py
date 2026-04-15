from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.note import NoteCreateIn, NoteOut, NoteUpdateIn
from app.schemas.request import NoteIDRequest
from app.schemas.response import ResponseModel
from app.services import *
from app.utils.response import fail_not_found, ok, ok_created, ok_no_content


note_router = APIRouter(prefix="/note", tags=["笔记API"])


@note_router.post("/create", response_model=ResponseModel[NoteOut])
async def create_note(
    payload: NoteCreateIn,
    current_user: User = Depends(get_current_user),
) -> ResponseModel[NoteOut]:
    note = await Service.note.create_note(
        user=current_user,
        category_id=payload.category_id,
        title=payload.title,
        content=payload.content,
        tags=payload.tags,
        starred=payload.starred,
    )
    return ok_created(
        data=NoteOut(
            id=note.id,
            category_id=payload.category_id,
            category_name=note.category_name,
            title=note.title,
            content=note.content,
            tags=note.tags,
            starred=note.starred,
            created_at=note.created_at,
            updated_at=note.updated_at,
        ),
        message="笔记创建成功",
    )


@note_router.post("/update", response_model=ResponseModel[NoteOut])
async def update_note(
    payload: NoteUpdateIn,
    current_user: User = Depends(get_current_user),
) -> ResponseModel[NoteOut]:
    note = await Service.note.update_note(
        user=current_user,
        note_id=payload.id,
        category_id=payload.category_id,
        title=payload.title,
        content=payload.content,
        tags=payload.tags,
        starred=payload.starred,
    )
    if note is None:
        return fail_not_found(message="笔记不存在或无权限")

    return ok(
        data=NoteOut(
            id=note.id,
            category_id=payload.category_id,
            category_name=note.category_name,
            title=note.title,
            content=note.content,
            tags=note.tags,
            starred=note.starred,
            created_at=note.created_at,
            updated_at=note.updated_at,
        ),
        message="笔记更新成功",
    )


@note_router.post("/delete", response_model=ResponseModel[None])
async def delete_note(
    payload: NoteIDRequest,
    current_user: User = Depends(get_current_user),
) -> ResponseModel[None]:
    deleted = await Service.note.delete_note(user=current_user, note_id=payload.id)
    if not deleted:
        return fail_not_found(message="笔记不存在或无权限")
    return ok_no_content(message="笔记删除成功")


@note_router.get("/list", response_model=ResponseModel[list[NoteOut]])
async def list_notes(
    current_user: User = Depends(get_current_user),
) -> ResponseModel[list[NoteOut]]:
    notes = await Service.note.list_notes(user=current_user)
    data = [
        NoteOut(
            id=n.id,
            category_id=(n.category.category_id if n.category else None),
            category_name=n.category_name,
            title=n.title,
            content=n.content,
            tags=n.tags,
            starred=n.starred,
            created_at=n.created_at,
            updated_at=n.updated_at,
        )
        for n in notes
    ]
    return ok(data=data, message="获取笔记列表成功")