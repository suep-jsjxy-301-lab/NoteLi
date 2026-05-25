from langchain.tools import ToolRuntime, tool
from app.agents.model import NoteModel
from app.models.models import Note
from app.services import Service
from app.agents.State import ContextState

@tool("create_note", return_direct=False)
async def create_note_tool(
    runtime: ToolRuntime[ContextState],
) -> Note:
    """
    创建笔记工具
    注意：新建笔记不需要参数，
    调用该工具后，将返回的notemodel添加进context中
    """
    user_id = runtime.context.get("user_id")
    user = await Service.user.get_user_by_id(user_id)
    note = await Service.note.create_note(
        user=user,
        category_id=2,
        title="",
        content="",
        tags=[],
        starred=False,
    )
    notemodel = NoteModel(
        note_id=note.id,
        user_id=note.user_id,
        category_id=note.category_id,
        title=note.title,
        content=note.content,
        tags=note.tags,
        starred=note.starred
    )
    return notemodel

@tool("update_note", return_direct=False)
async def update_note_tool(
    runtime: ToolRuntime[ContextState],
    note_id: int,
    title: str,
    content: str,
    category_id: int,
    tags: list[str],
    starred: bool,
) -> NoteModel:
    """
    更新笔记工具
    注意：更新笔记前需要确认context中是否有该notemodel,如果没有则需要先调用搜索笔记工具将该notemodel放进context中
    除了要修改的字段外，其他字段需要保持不变
    调用该工具后，将返回的notemodel添加进context中，并替换掉更新使用的notemodel
    """
    user_id = runtime.context.get("user_id")
    user = await Service.user.get_user_by_id(user_id)
    note = await Service.note.update_note(
        user=user,
        note_id=note_id,
        category_id=category_id,
        title=title,
        content=content,
        tags=tags,
        starred=starred,
    )
    notemodel = NoteModel(
        note_id=note.id,
        user_id=note.user_id,
        category_id=note.category_id,
        title=note.title,
        content=note.content,
        tags=note.tags,
        starred=note.starred
    )
    return notemodel

@tool("search_notes", return_direct=False)
async def search_notes_tool(
    runtime: ToolRuntime[ContextState],
) -> list[NoteModel]:
    """
    搜索笔记工具
    注意：该工具用于搜索用户所有的笔记，返回值为笔记列表
    调用该工具后，只将需要的notemodel放进context中,不需要的笔记不要放入context,供后续步骤使用
    """
    user_id = runtime.context.get("user_id")
    notes = await Service.note.list_notes(user=await Service.user.get_user_by_id(user_id))
    notemodels = []
    for note in notes:
        notemodel = NoteModel(
            note_id=note.id,
            user_id=note.user_id,
            category_id=note.category_id,
            title=note.title,
            content=note.content,
            tags=note.tags,
            starred=note.starred
        )
        notemodels.append(notemodel)
    return notemodels

@tool("delete_note", return_direct=False)
async def delete_note_tool(
    runtime: ToolRuntime[ContextState],
    note_id: int,
) -> bool:
    """
    删除笔记工具
    注意：删除笔记前需要确认context中是否有该notemodel,如果没有notemodel则需要先调用搜索笔记工具将该notemodel放进context中
    若没有搜索到目标笔记的notemodel则不要调用删除工具
    调用该工具后，将该notemodel从context中删除
    """
    user_id = runtime.context.get("user_id")
    user = await Service.user.get_user_by_id(user_id)
    result = await Service.note.delete_note(
        user=user,
        note_id=note_id,
    )
    return result