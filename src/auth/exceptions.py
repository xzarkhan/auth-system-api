from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Not authenticated", scheme: str = "Bearer"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": scheme},
        )


class AccountDeactivatedException(HTTPException):
    def __init__(self, detail: str = "This account is deactivated"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
