# app/api/v1/category.py

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.response import ResponseModel
from app.schemas.category import CategoryIn, CategoryOut
from app.services import *
from app.schemas.request import CategoryIDRequest
from app.utils.response import fail_conflict, ok, ok_created

category_router = APIRouter(
    prefix="/category",
    tags=["分类API"],
)

@category_router.post("/create", response_model=ResponseModel[CategoryOut])
async def create_category(
    payload: CategoryIn,
    current_user: User = Depends(get_current_user)
) -> ResponseModel[CategoryOut]:
    """
    创建新分类接口。
    接收分类ID和分类名称，创建新分类。
    Args:
        payload: 包含 category_id 和 category_name 的请求体。
    Returns:
        统一响应包装，data 字段为 CategoryOut 模型，包含新分类信息。
    Raises:
        HTTPException: 409 分类名称已存在。
    """
    if await Service.category.get_category_by_user_and_category_name(current_user, payload.category_name):
        return fail_conflict(message="分类名称已存在")

    category = await Service.category.create_category(
        user=current_user,
        category_id=payload.category_id,
        category_name=payload.category_name,
    )
    if category is None:
        return fail_conflict(message="分类创建失败")

    return ok_created(
        data=CategoryOut(
            id=category.id,
            category_id=category.category_id,
            category_name=category.category_name,
        ),
        message="分类创建成功",
    )

@category_router.get("/list", response_model=ResponseModel[list[CategoryOut]])
async def list_categories(
    current_user: User = Depends(get_current_user)
) -> ResponseModel[list[CategoryOut]]:
    """
    获取用户分类列表接口。
    Args:
        current_user: 当前认证用户，由依赖注入提供。
    Returns:
        统一响应包装，data 字段为 CategoryOut 模型列表，包含用户的所有分类信息。
    """
    categories = await Service.category.get_categories_by_user(current_user)
    category_out_list = [
        CategoryOut(
            id=category.id,
            category_id=category.category_id,
            category_name=category.category_name,
        )
        for category in categories
    ]
    return ok(data=category_out_list, message="获取分类列表成功")

@category_router.post("/delete", response_model=ResponseModel[None])
async def delete_category(
    id: CategoryIDRequest,
) -> ResponseModel[None]:
    """
    删除分类接口。
    接收分类ID，删除对应分类。
    Args:
        id: 包含分类ID的请求体。
    Returns:
        统一响应包装，无 data 字段，包含删除成功消息。
    Raises:
        HTTPException: 404 分类不存在或不属于当前用户。
    """
    category = await Service.category.get_category_by_id(id.id)
    if category is None:
        return fail_conflict(message="分类不存在或不属于当前用户")
    await Service.category.delete_category(id.id)
    return ok(message="分类删除成功")

@category_router.post("/update/{category_id}", response_model=ResponseModel[CategoryOut])
async def update_category(
    category_id: int,
    payload: CategoryIn,
) -> ResponseModel[CategoryOut]:
    """
    更新分类接口。
    接收分类ID和新的分类信息，更新对应分类。
    Args:
        category_id: 分类ID。
        payload: 包含新的 category_id 和 category_name 的请求体。
    Returns:
        统一响应包装，data 字段为 CategoryOut 模型，包含更新后的分类
    Raises:        
        HTTPException: 404 分类不存在或不属于当前用户。
    """
    category = await Service.category.get_category_by_id(category_id)
    if category is None:
        return fail_conflict(message="分类不存在或不属于当前用户")

    updated_category = await Service.category.update_category(
        id=category_id,
        new_category_id=payload.category_id,
        new_category_name=payload.category_name,
    )
    if updated_category is None:
        return fail_conflict(message="分类更新失败")

    return ok(
        data=CategoryOut(
            id=updated_category.id,
            category_id=updated_category.category_id,
            category_name=updated_category.category_name,
        ),
        message="分类更新成功",
    )