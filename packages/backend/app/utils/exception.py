from fastapi import HTTPException
from typing import Any


class BizHTTPException(HTTPException):
    """
    业务异常，统一内部 code/message，可带 details
    """

    def __init__(
        self,
        *,
        error_code: int = 400,
        message: str,
        status_code: int = 400,
        details: Any = None,
    ):
        super().__init__(status_code=status_code, detail=message)
        self.error_code = error_code
        self.details = details
