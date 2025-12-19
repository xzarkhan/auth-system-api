from typing import Annotated
from fastapi import APIRouter, Body, Depends, Path

from src.permissions.dependencies import GetPermissionServiceDep
from src.permissions.service import PermissionService
from src.permissions.schemas import (
    AssignPermissionSchema,
    PermissionCreateSchema,
    PermissionDeleteSchema,
    PermissionResponseSchema,
    RevokePermissionSchema,
)

from src.auth.dependencies import PermissionDep


router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.get(
    "",
    response_model=list[PermissionResponseSchema],
    status_code=200,
    dependencies=[
        Depends(
            PermissionDep(
                ["permissions:read", "permissions:full_access"], required_all=False
            )
        )
    ],
)
async def get_all_permissions(
    permission_service: Annotated[PermissionService, Depends(GetPermissionServiceDep)],
):
    return await permission_service.get_all()


@router.get(
    "/{role_name}",
    response_model=list[PermissionResponseSchema],
    status_code=200,
    dependencies=[
        Depends(
            PermissionDep(
                ["permissions:read", "permissions:full_access"], required_all=False
            )
        )
    ],
)
async def get_role_permissions(
    role_name: Annotated[str, Path()],
    permission_service: Annotated[PermissionService, Depends(GetPermissionServiceDep)],
):
    return await permission_service.get_role_permissions(role_name=role_name)


@router.post(
    "",
    response_model=PermissionResponseSchema,
    status_code=201,
    dependencies=[
        Depends(
            PermissionDep(
                ["permissions:create", "permissions:full_access"], required_all=False
            )
        )
    ],
)
async def create_permission(
    permission_data: Annotated[PermissionCreateSchema, Body()],
    permission_service: Annotated[PermissionService, Depends(GetPermissionServiceDep)],
):
    return await permission_service.create(permission_data)


@router.post(
    "/{role_name}/assign",
    response_model=list[PermissionResponseSchema],
    status_code=200,
    dependencies=[
        Depends(
            PermissionDep(
                ["permissions:assign", "permissions:full_access"], required_all=False
            )
        )
    ],
)
async def assign_permission_to_role(
    role_name: Annotated[str, Path()],
    assign_data: Annotated[AssignPermissionSchema, Body()],
    permission_service: Annotated[PermissionService, Depends(GetPermissionServiceDep)],
):
    return await permission_service.assign_permission_to_role(
        role_name=role_name, assign_data=assign_data
    )


@router.post(
    "/{role_name}/revoke",
    response_model=list[PermissionResponseSchema],
    status_code=200,
    dependencies=[
        Depends(
            PermissionDep(
                ["permissions:revoke", "permissions:full_access"], required_all=False
            )
        )
    ],
)
async def revoke_permission_from_role(
    role_name: Annotated[str, Path()],
    revoke_data: Annotated[RevokePermissionSchema, Body()],
    permission_service: Annotated[PermissionService, Depends(GetPermissionServiceDep)],
):
    return await permission_service.revoke_permission_from_role(
        role_name=role_name, revoke_data=revoke_data
    )


@router.delete(
    "",
    response_model=PermissionResponseSchema,
    status_code=200,
    dependencies=[
        Depends(
            PermissionDep(
                ["permissions:delete", "permissions:full_access"], required_all=False
            )
        )
    ],
)
async def delete_permission(
    permission_data: Annotated[PermissionDeleteSchema, Body()],
    permission_service: Annotated[PermissionService, Depends(GetPermissionServiceDep)],
):
    return await permission_service.delete(permission_data)
