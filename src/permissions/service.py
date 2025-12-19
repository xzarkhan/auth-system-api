from src.permissions.repository import PermissionRepository
from src.permissions.models import Permission
from src.permissions.schemas import (
    AssignPermissionSchema,
    PermissionCreateSchema,
    PermissionDeleteSchema,
    RevokePermissionSchema,
)

from src.exceptions.exceptions import AlreadyExistsException, ForbiddenException, NotFoundException

from src.users.repositories import RoleRepository
from src.users.models import Role


class PermissionService:
    def __init__(self, role_repo: RoleRepository, permission_repo: PermissionRepository) -> None:
        self.permission_repo = permission_repo
        self.role_repo = role_repo

    async def get_all(self) -> list[Permission]:
        return await self.permission_repo.get_all()

    async def get_role_permissions(self, role_name: str) -> list[Permission]:
        role = await self.role_repo.get_by_name(name=role_name)
        if not role:
            raise NotFoundException(detail=f"Role '{role_name}' not found")

        return role.permissions

    async def create(self, permission_data: PermissionCreateSchema) -> Permission:
        if await self.permission_repo.get_by_name(name=permission_data.name):
            raise AlreadyExistsException(detail=f"Permission {permission_data.name} already exists")

        new_permission = await self.permission_repo.create(data=permission_data.model_dump())

        await self.permission_repo.session.commit()
        await self.permission_repo.session.refresh(new_permission)

        return new_permission

    async def delete(self, permission_data: PermissionDeleteSchema) -> Permission:
        permission = await self.permission_repo.get_by_name(name=permission_data.name)
        if not permission:
            raise NotFoundException(detail=f"Permission '{permission_data.name}' not found")

        await self.permission_repo.delete(id=permission.id)
        await self.permission_repo.session.commit()

        return permission

    async def assign_permission_to_role(
        self, role_name: str, assign_data: AssignPermissionSchema
    ) -> list[Permission]:
        role = await self.role_repo.get_by_name(name=role_name)
        permission = await self.permission_repo.get_by_name(name=assign_data.permission_name)

        if not role or not permission:
            raise NotFoundException(detail="Role or permission not found")

        if permission not in role.permissions:
            role.permissions.append(permission)
            await self.role_repo.session.commit()

        return role.permissions

    async def revoke_permission_from_role(
        self, role_name: str, revoke_data: RevokePermissionSchema
    ) -> list[Permission]:
        role = await self.role_repo.get_by_name(name=role_name)
        permission = await self.permission_repo.get_by_name(name=revoke_data.permission_name)

        if not role or not permission:
            raise NotFoundException(detail="Role or permission not found")

        if permission in role.permissions:
            role.permissions.remove(permission)
            await self.role_repo.session.commit()

        return role.permissions

    async def check_permissions(
        self, role: Role, permissions: list[str], required_all: bool
    ) -> None:
        role_permissions = {permission.name for permission in role.permissions}
        
        if required_all:
            for permission in permissions:
                if permission not in role_permissions:
                    raise ForbiddenException()
        else:
            for permission in permissions:
                if permission in role_permissions:
                    return
            raise ForbiddenException()
