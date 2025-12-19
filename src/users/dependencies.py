from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.core.database import get_session

from src.users.repositories import RoleRepository, UserRepository
from src.users.service import UserService


async def GetUserServiceDep(session: AsyncSession = Depends(get_session)) -> UserService:
    user_repo = UserRepository(session)
    role_repo = RoleRepository(session)
    return UserService(user_repo=user_repo, role_repo=role_repo)
