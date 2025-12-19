from fastapi import Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from src.permissions.dependencies import GetPermissionServiceDep
from src.permissions.service import PermissionService
from src.auth.exceptions import AccountDeactivatedException
from src.auth.service import AuthService
from src.users.dependencies import GetUserServiceDep
from src.auth.service import AuthService
from src.users.models import User
from src.users.service import UserService

security_bearer_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def GetAuthServiceDep(
    user_service: Annotated[UserService, Depends(GetUserServiceDep)],
) -> AuthService:
    return AuthService(user_service)


async def AuthenticateUserDep(
    token: Annotated[str, Depends(security_bearer_scheme)],
    auth_service: Annotated[AuthService, Depends(GetAuthServiceDep)],
) -> User:
    current_user = await auth_service.get_current_user(token=token)
    if not current_user.is_active:
        raise AccountDeactivatedException()
    return current_user


class PermissionDep:
    def __init__(self, permissions: list[str], required_all: bool = True) -> None:
        self.permissions = permissions
        self.required_all = required_all

    async def __call__(
        self,
        current_user: Annotated[User, Depends(AuthenticateUserDep)],
        permission_service: Annotated[
            PermissionService, Depends(GetPermissionServiceDep)
        ],
    ) -> None:
        await permission_service.check_permissions(
            role=current_user.role,
            permissions=self.permissions,
            required_all=self.required_all,
        )
