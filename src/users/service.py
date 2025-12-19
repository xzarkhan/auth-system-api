from src.users.repositories import RoleRepository, UserRepository
from src.users.models import User
from src.users.schemas import (
    RoleAssignSchema, 
    UserCreateSchema, 
    UserPartialUpdateSchema, 
    UserUpdateSchema
)

from src.core.config import settings
from src.core.security import hash_password

from src.exceptions.exceptions import AlreadyExistsException
from src.exceptions.exceptions import NotFoundException


class UserService:
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository) -> None:
        self.user_repo = user_repo
        self.role_repo = role_repo

    async def get_all(self) -> list[User]:
        return await self.user_repo.get_all()

    async def get_by_id(self, user_id: int) -> User:
        if (user := await self.user_repo.get(id=user_id)):
            return user
        raise NotFoundException(detail=f"User with id={user_id} not found")

    async def get_by_email(self, user_email: str) -> User:
        if (user := await self.user_repo.get_by_email(email=user_email)):
            return user
        raise NotFoundException(detail=f"User with email={user_email} not found")
    
    async def create(self, user_data: UserCreateSchema) -> User:
        try:
            if await self.get_by_email(user_email=user_data.email):
                raise AlreadyExistsException(
                    detail=f"User with email={user_data.email} already exists"
                )
        except NotFoundException:
            pass

        new_user_data = user_data.model_dump(exclude={"password"})
        new_user_data["hashed_password"] = hash_password(password=user_data.password)

        default_role = await self.role_repo.get_by_name(name=settings.DEFAULT_USER_ROLE)

        new_user_data["role_id"] = default_role.id
        new_user = await self.user_repo.create(data=new_user_data)

        await self.user_repo.session.commit()
        await self.user_repo.session.refresh(new_user)

        return new_user

    async def update_user_role(
        self,
        user_email: str,
        role_name: str,
    ) -> User:
        user = await self.get_by_email(user_email=user_email)

        role = await self.role_repo.get_by_name(name=role_name)
        if not role:
            raise NotFoundException(detail=f"Role '{role_name}' not found")
        
        await self.user_repo.update(id=user.id, data={"role_id": role.id})

        await self.user_repo.session.commit()
        await self.user_repo.session.refresh(user)

        return user

    async def update(
        self,
        user_id: int,
        update_data: UserUpdateSchema | UserPartialUpdateSchema,
        partial: bool = True,
    ) -> User:
        data_to_update = update_data.model_dump(exclude_unset=partial)

        if "email" in data_to_update:
            existing = await self.user_repo.get_by_email(email=data_to_update["email"])
            if (existing) and (existing.id != user_id):
                raise AlreadyExistsException(detail=f"Email {existing.email} already use")

        if "password" in data_to_update:
            data_to_update["hashed_password"] = hash_password(
                data_to_update.pop("password")
            )

        updated_user = await self.user_repo.update(id=user_id, data=data_to_update)

        await self.user_repo.session.commit()
        await self.user_repo.session.refresh(updated_user)

        return updated_user

    async def deactivate_account(self, user_id: int) -> User:
        user = await self.get_by_id(user_id=user_id)

        await self.user_repo.update(id=user_id, data={"is_active": False})
        await self.user_repo.session.commit()

        return user
