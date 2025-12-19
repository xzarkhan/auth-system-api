from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.base_repository import SQLARepository

from src.users.models import Role, User


class UserRepository(SQLARepository):
    model = User

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_email(self, email: str):
        result = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return result.scalar_one_or_none()


class RoleRepository(SQLARepository):
    model = Role
