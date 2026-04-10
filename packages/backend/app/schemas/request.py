from pydantic import BaseModel

class VerifyPasswordRequest(BaseModel):
    password: str