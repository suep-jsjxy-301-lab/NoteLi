import asyncio

from langchain.tools import ToolRuntime, tool
from app.agents.model import CategoryModel
from app.services import Service
from app.agents.State import ContextState

@tool("create_category", return_direct=False)
async def create_category_tool(
    runtime : ToolRuntime[ContextState],
    category_id: int,
    category_name : str
):
    """
    创建分类工具
    注意:category_id可以通过工具获取,category_name从用户需求获取,
    若用户未指定图标(图案)样式,则默认category_id = 2,
    该用户的分类中category_name不能有重复
    调用该工具后，将返回的categorymodel添加进context中
    """
    user_id = runtime.context.get("user_id")
    user = await Service.user.get_user_by_id(user_id)
    category = await Service.category.create_category(
        user = user,
        category_id=category_id,
        category_name=category_name
    )
    return CategoryModel(
        id = category.id,
        category_id = category.category_id,
        category_name = category.category_name
    )

@tool("update_category",return_direct=False)
async def update_category_tool(
    id : int,
    category_id : int,
    category_name : str,
):
    """
    修改分类工具
    注意:id 1到5的分类是默认分类,禁止修改,
    该用户的分类名称不能存在相同,
    调用后将修改的categorymodel,覆盖原有的categorymodel,存入context
    """
    if(id in [1,2,3,4,5]):
        return "默认分类禁止更新"
    else:
        isUpdate = Service.category.update_category(
            id=id,
            new_category_id=category_id,
            new_category_name=category_name,
        )
        if not isUpdate:
            return "更新失败"
        category = await Service.category.get_category_by_id(id)
        return CategoryModel(
            id = category.id,
            category_id = category.category_id,
            category_name = category.category_name,
        )

@tool("delete_category",return_direct=False)
async def delete_category_tool(
    id : int
):
    """
    删除分类工具
    注意:id 1到5的分类是默认分类,禁止删除,
    删除前需确认该分类属于用户,
    若删除前该分类有笔记,需现将笔记移至默认分类,即id=2
    删除后将使用的categorymodel移出context
    """
    if (id in [1,2,3,4,5]):
        return "默认分类禁止删除"
    else:
        isDelete = await Service.category.delete_category(id)
        if not isDelete:
            return "删除失败"
        else:
            return "删除成功"


@tool("search_categories", return_direct=False)
async def search_categories_tool(
    runtime: ToolRuntime[ContextState],
):
    """
    搜索分类工具
    注意：该工具用于搜索用户所有的分类，返回值为分类列表
    调用该工具后，只将需要的categorymodel放进context中,不需要的分类不要放入context,供后续步骤使用
    """
    user_id = runtime.context.get("user_id")
    user = await Service.user.get_user_by_id(user_id) 
    default_categories = await Service.category.get_default_categories()
    user_categories = await Service.category.get_categories_by_user(user)
    categories = default_categories + user_categories
    return [CategoryModel(
        id = category.id,
        category_id = category.category_id,
        category_name = category.category_name,
    ) for category in categories]

@tool("get_default_icon",return_direct=False)
async def get_default_icon_tool():
    """
    获取分类图标工具
    注意:category_id的值为图标的位置,初始为1,
    不能作为步骤名,配合其他工具使用
    """
    default_icon = [
    '📋', '💼', '🏠', '📚', '💡', '✅', 
    '🎯', '🎨', '🎵', '🏃', '🍔', '✈️',
    '📷', '🎮', '❤️', '🌟', '🔥', '💻',
    '📝', '🔧', '🎓', '🏆', '💎', '🌍'
    ]
    return default_icon