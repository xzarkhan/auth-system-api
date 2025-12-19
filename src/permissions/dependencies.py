from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.permissions.repository import PermissionRepository
from src.permissions.service import PermissionService

from src.users.repositories import RoleRepository

from src.core.database import get_session


async def GetPermissionServiceDep(
    session: AsyncSession = Depends(get_session),
) -> PermissionService:
    permission_repo = PermissionRepository(session)
    role_repo = RoleRepository(session)
    return PermissionService(role_repo=role_repo, permission_repo=permission_repo)
