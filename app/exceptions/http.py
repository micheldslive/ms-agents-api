from fastapi import HTTPException


class SystemHttpException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str | dict | None = None,
        error_code: str | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
