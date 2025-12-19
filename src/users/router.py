from fastapi import APIRouter, Body, Depends
from typing import Annotated

from src.auth.dependencies import AuthenticateUserDep, PermissionDep

from src.users.dependencies import GetUserServiceDep
from src.users.service import UserService
from src.users.models import User
from src.users.schemas import (
    RoleAssignSchema,
    RoleResponseSchema,
    UserResponseSchema,
    UserPartialUpdateSchema,
    UserUpdateSchema,
)


router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=list[UserResponseSchema],
    status_code=200,
    dependencies=[
        Depends(PermissionDep(["users:read", "users:full_access"], required_all=False))
    ],
)
async def get_all_users(user_service: Annotated[UserService, Depends(GetUserServiceDep)]):
    return await user_service.get_all()


@router.get("/me", response_model=UserResponseSchema, status_code=200)
async def get_my_info(current_user: Annotated[User, Depends(AuthenticateUserDep)]):
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
    status_code=200,
    dependencies=[
        Depends(PermissionDep(["users:read", "users:full_access"], required_all=False))
    ],
)
async def get_user_by_email(
    user_email: str, user_service: Annotated[UserService, Depends(GetUserServiceDep)]
):
    return await user_service.get_by_email(user_email=user_email)


@router.post(
    "/assign-role", 
    response_model=UserResponseSchema, 
    status_code=200,
    dependencies=[
        Depends(
            PermissionDep(
                ["permissions:assign", "permissions:full_access"], required_all=False
            )
        )
    ],   
)
async def assign_role(
    assign_data: Annotated[RoleAssignSchema, Body()],
    user_service: Annotated[UserService, Depends(GetUserServiceDep)],
):
    return await user_service.update_user_role(
        user_email=assign_data.user_email, role_name=assign_data.role_name
    )


@router.patch("/me", response_model=UserResponseSchema, status_code=200)
async def partial_update_my_profile(
    current_user: Annotated[User, Depends(AuthenticateUserDep)],
    user_data: Annotated[UserPartialUpdateSchema, Body()],
    user_service: Annotated[UserService, Depends(GetUserServiceDep)],
):
    return await user_service.update(
        user_id=current_user.id, update_data=user_data, partial=True
    )


@router.put("/me", response_model=UserResponseSchema, status_code=200)
async def update_my_profile(
    current_user: Annotated[User, Depends(AuthenticateUserDep)],
    user_data: Annotated[UserUpdateSchema, Body()],
    user_service: Annotated[UserService, Depends(GetUserServiceDep)],
):
    return await user_service.update(
        user_id=current_user.id, update_data=user_data, partial=False
    )


@router.delete("/me", response_model=UserResponseSchema, status_code=200)
async def deactivate_my_account(
    current_user: Annotated[User, Depends(AuthenticateUserDep)],
    user_service: Annotated[UserService, Depends(GetUserServiceDep)],
):
    return await user_service.deactivate_account(user_id=current_user.id)
