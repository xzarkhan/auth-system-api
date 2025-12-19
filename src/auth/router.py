from fastapi import APIRouter, Body, Depends, Request, Response
from typing import Annotated

from src.auth.dependencies import GetAuthServiceDep
from src.auth.service import AuthService
from src.auth.schemas import (
    AuthCredentialsSchema,
    LogoutResponseSchema,
    TokenResponseSchema,
)

from src.users.schemas import UserCreateSchema, UserResponseSchema



router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponseSchema, status_code=200)
async def login(
    response: Response,
    auth_credetials: Annotated[AuthCredentialsSchema, Body()],
    auth_service: Annotated[AuthService, Depends(GetAuthServiceDep)],
):
    return await auth_service.login(credentials=auth_credetials, response=response)


@router.post("/register", response_model=UserResponseSchema, status_code=201)
async def register(
    user_data: Annotated[UserCreateSchema, Body()],
    auth_service: Annotated[AuthService, Depends(GetAuthServiceDep)],
):
    return await auth_service.register(user_data=user_data)


@router.post("/refresh", response_model=TokenResponseSchema, status_code=200)
async def refresh(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(GetAuthServiceDep),
):
    return await auth_service.refresh(request=request, response=response)


@router.post("/logout", response_model=LogoutResponseSchema, status_code=200)
async def logout(
    request: Request,
    response: Response,
    auth_service: Annotated[AuthService, Depends(GetAuthServiceDep)],
):
    return await auth_service.logout(request=request, response=response)
