# app/api/v1/user.py

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user
from app.models.models import User
from app.schemas.response import ResponseModel
from app.schemas.user import UserOut
from app.utils.response import ok

user_router = APIRouter(
    prefix="/user",
    tags=["用户API"],
)


@user_router.get("/me", response_model=ResponseModel[UserOut])
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> ResponseModel[UserOut]:
    return ok(
        data=UserOut(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            phone=current_user.phone,
        )
    )

