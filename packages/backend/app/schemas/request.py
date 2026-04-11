from pydantic import BaseModel, Field

class VerifyPasswordRequest(BaseModel):
    password: str

class ChangePasswordRequest(BaseModel):
    new_password: str = Field(default=..., min_length=6, max_length=128)