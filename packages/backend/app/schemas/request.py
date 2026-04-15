from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class VerifyPasswordRequest(BaseModel):
    password: str

class ChangePasswordRequest(BaseModel):
    new_password: str = Field(default=..., min_length=6, max_length=128)

class ChangeEmailRequest(BaseModel):
    new_email: EmailStr = Field(default=..., max_length=255)

class ChangePhoneRequest(BaseModel):
    new_phone: Optional[str] = Field(default=None, max_length=16)

class ChangeUsernameRequest(BaseModel):
    new_username: str = Field(default=..., min_length=3, max_length=64)

class CategoryIDRequest(BaseModel):
    id: int = Field(default=..., gt=0)

class NoteIDRequest(BaseModel):
    id: int = Field(default=..., ge=1)