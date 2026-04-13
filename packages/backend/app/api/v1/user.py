# app/api/v1/user.py

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.response import ResponseModel
from app.schemas.user import UserIn, UserOut
from app.schemas.request import ChangePasswordRequest, ChangeEmailRequest, ChangePhoneRequest, ChangeUsernameRequest
from app.services.user import UserService
from app.utils.response import fail_conflict, ok, ok_created

user_router = APIRouter(
    prefix="/user",
    tags=["用户API"],
)


@user_router.post("/register", response_model=ResponseModel[UserOut])
async def register_user(payload: UserIn) -> ResponseModel[UserOut]:
    """
    用户注册接口。
    接收用户名、密码、邮箱和可选的手机号，创建新用户。
    Args:
        payload: 包含 username、password、email 和可选 phone 的请求体。
    Returns:
        统一响应包装，data 字段为 UserOut 模型，包含新用户信息。
    Raises:
        HTTPException: 409 用户名、邮箱或手机号已存在。
    """
    if await UserService.get_user_by_username(payload.username):
        return fail_conflict(message="用户名已存在")
    if await UserService.get_user_by_email(payload.email):
        return fail_conflict(message="邮箱已存在")
    if payload.phone and await UserService.get_user_by_phone(payload.phone):
        return fail_conflict(message="手机号已存在")

    user = await UserService.create_user(
        username=payload.username,
        password=payload.password,
        email=payload.email,
        phone=payload.phone,
    )
    if user is None:
        return fail_conflict(message="用户注册失败")

    return ok_created(
        data=UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            phone=user.phone,
        ),
        message="注册成功",
    )


@user_router.get("/me", response_model=ResponseModel[UserOut])
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> ResponseModel[UserOut]:
    """
    获取当前登录用户的个人信息。
    需要在请求头中携带有效的 Bearer token 进行身份验证。
    Args:
        current_user: 通过依赖注入获取当前用户对象。
    Returns:
        统一响应包装，data 字段为 UserOut 模型，包含当前用户信息。
    Raises:
        HTTPException: 401 如果 token 无效或用户不存在。
    """
    return ok(
        data=UserOut(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            phone=current_user.phone,
        )
    )

@user_router.post("/delete", response_model=ResponseModel[None])
async def delete_current_user(
    current_user: User = Depends(get_current_user),
) -> ResponseModel[None]:
    """
    注销当前登录用户的账户。
    需要在请求头中携带有效的 Bearer token 进行身份验证。
    Args:
        current_user: 通过依赖注入获取当前用户对象。
    Returns:
        成功消息。
    Raises:
        HTTPException: 401 如果 token 无效或用户不存在；400 如果删除失败。
    """
    success = await UserService.delete_user(current_user.id)
    if not success:
        return fail_conflict(message="用户删除失败")
    return ok(message="用户删除成功")

@user_router.post("/change-password", response_model=ResponseModel[bool])
async def change_password(
    new_password: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
) -> ResponseModel[bool]:
    """
    修改当前登录用户的密码。
    需要在请求头中携带有效的 Bearer token 进行身份验证。
    Args:
        new_password: 包含新密码的请求体。
        current_user: 通过依赖注入获取当前用户对象。
    Returns:
        统一响应包装，data 字段为布尔值，表示密码修改是否成功。
    Raises:
        HTTPException: 401 如果 token 无效或用户不存在；400 如果密码修改失败。
    """
    success = await UserService.update_password(current_user.id, new_password.new_password)
    if not success:
        return fail_conflict(message="密码修改失败")
    return ok(data=True, message="密码修改成功")

@user_router.post("/change-email", response_model=ResponseModel[bool])
async def change_email(
    new_email: ChangeEmailRequest,
    current_user: User = Depends(get_current_user),
) -> ResponseModel[bool]:
    """
    修改当前登录用户的邮箱地址。
    需要在请求头中携带有效的 Bearer token 进行身份验证。
    Args:
        new_email: 包含新邮箱地址的请求体。
        current_user: 通过依赖注入获取当前用户对象。
    Returns:
        统一响应包装，data 字段为布尔值，表示邮箱修改是否成功
    Raises:
        HTTPException: 401 如果 token 无效或用户不存在；400 如果邮箱修改失败
    """
    if await UserService.get_user_by_email(new_email.new_email):
        return fail_conflict(message="邮箱已存在")
    success = await UserService.update_email(current_user.id, new_email.new_email)
    if not success:
        return fail_conflict(message="邮箱修改失败")
    return ok(data=True, message="邮箱修改成功")

@user_router.post("/change-phone", response_model=ResponseModel[bool])
async def change_phone(
    new_phone: ChangePhoneRequest,
    current_user: User = Depends(get_current_user),
) -> ResponseModel[bool]:
    """
    修改当前登录用户的手机号。
    需要在请求头中携带有效的 Bearer token 进行身份验证。
    Args:
        new_phone: 包含新手机号的请求体。
        current_user: 通过依赖注入获取当前用户对象。
    Returns:
        统一响应包装，data 字段为布尔值，表示手机号修改是否成功
    Raises:
        HTTPException: 401 如果 token 无效或用户不存在；400 如果手机号修改失败
    """
    if await UserService.get_user_by_phone(new_phone.new_phone):
        return fail_conflict(message="手机号已存在")
    success = await UserService.update_phone(current_user.id, new_phone.new_phone)
    if not success:
        return fail_conflict(message="手机号修改失败")
    return ok(data=True, message="手机号修改成功")

@user_router.post("/change-username", response_model=ResponseModel[bool])
async def change_username(
    new_username: ChangeUsernameRequest,
    current_user: User = Depends(get_current_user),
) -> ResponseModel[bool]:
    """
    修改当前登录用户的用户名。
    需要在请求头中携带有效的 Bearer token 进行身份验证。
    Args:
        new_username: 包含新用户名的请求体。
        current_user: 通过依赖注入获取当前用户对象。
    Returns:
        统一响应包装，data 字段为布尔值，表示用户名修改是否成功。
    Raises:
        HTTPException: 401 如果 token 无效或用户不存在；400 如果用户名修改失败。
    """
    if await UserService.get_user_by_username(new_username.new_username):
        return fail_conflict(message="用户名已存在")
    success = await UserService.update_username(current_user.id, new_username.new_username)
    if not success:
        return fail_conflict(message="用户名修改失败")
    return ok(data=True, message="用户名修改成功")