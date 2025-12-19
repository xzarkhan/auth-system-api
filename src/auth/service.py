from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Request, Response
from datetime import timedelta

from src.auth.blacklist import TokensRedisBlacklist
from src.auth.exceptions import UnauthorizedException
from src.auth.schemas import (
    AuthCredentialsSchema,
    LogoutResponseSchema,
    TokenResponseSchema,
)

from src.core.jwt import decode_token, generate_access_token, generate_refresh_token
from src.core.security import verify_password
from src.core.config import settings

from src.users.schemas import UserCreateSchema
from src.users.service import UserService
from src.users.models import User


blacklist = TokensRedisBlacklist()


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    @staticmethod
    def issue_access_token(sub: int) -> str:
        payload = {"sub": str(sub)}
        access_token = generate_access_token(payload=payload)
        return access_token
    
    @staticmethod
    def issue_refresh_token(sub: int) -> str:
        payload = {"sub": str(sub)}
        refresh_token = generate_refresh_token(payload=payload)
        return refresh_token

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            payload = decode_token(token)
            sub = payload.get("sub")
            if not sub:
                raise UnauthorizedException(detail="Incorrect token payload")
            return payload
        except ExpiredSignatureError:
            raise UnauthorizedException(detail="Token expired")
        except InvalidTokenError:
            raise UnauthorizedException(detail="Invalid token")

    async def _validate_credentials(self, credentials: AuthCredentialsSchema) -> User:
        user = await self.user_service.get_by_email(user_email=credentials.email)
        if not user or not verify_password(
            password=credentials.password, hashed_password=user.hashed_password
        ):
            raise UnauthorizedException(detail="Incorrect email or password")
        return user

    async def _set_refresh_token_cookie(
        self, refresh_token: str, response: Response
    ) -> None:
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            path="/auth",
            secure=False,  # для localhost
            samesite="lax",
            max_age=int(
                timedelta(days=settings.JWT_REFRESH_TOKEN_EXP_DAYS).total_seconds()
            ),
        )

    async def refresh(self, request: Request, response: Response) -> TokenResponseSchema:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise UnauthorizedException(detail="No refresh token")

        payload = self.decode_token(token=refresh_token)

        jti = payload["jti"]
        if await blacklist.is_revoked(jti=jti):
            raise UnauthorizedException(detail="Refresh token revoked")

        sub = payload["sub"]
        new_access_token = self.issue_access_token(sub=sub)
        new_refresh_token = self.issue_refresh_token(sub=sub)

        await self._set_refresh_token_cookie(
            refresh_token=new_refresh_token, response=response
        )

        return TokenResponseSchema(access_token=new_access_token)

    async def get_current_user(self, token: str) -> User:
        payload = self.decode_token(token=token)
        user = await self.user_service.get_by_id(user_id=int(payload["sub"]))
        return user

    async def login(
        self, credentials: AuthCredentialsSchema, response: Response
    ) -> TokenResponseSchema:
        user = await self._validate_credentials(credentials=credentials)

        access_token = self.issue_access_token(sub=user.id)
        refresh_token = self.issue_refresh_token(sub=user.id)

        await self._set_refresh_token_cookie(
            refresh_token=refresh_token, response=response
        )

        return TokenResponseSchema(access_token=access_token)

    async def logout(self, request: Request, response: Response) -> LogoutResponseSchema:
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise UnauthorizedException(detail="No refresh token")

        payload = self.decode_token(token=refresh_token)

        jti = payload["jti"]
        expires_at = payload["exp"]
        await blacklist.revoke_token(jti=jti, expire_at=expires_at)

        response.delete_cookie(key="refresh_token", path="/auth")
        return LogoutResponseSchema()

    async def register(self, user_data: UserCreateSchema) -> User:
        new_user = await self.user_service.create(user_data=user_data)
        return new_user
