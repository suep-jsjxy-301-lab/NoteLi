from pydantic import BaseModel, Field

class MessageIn(BaseModel):
    message: str = Field(default=..., max_length=2000)