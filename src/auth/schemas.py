from pydantic import BaseModel


class AuthCredentialsSchema(BaseModel):
    email: str
    password: str


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class LogoutResponseSchema(BaseModel):
    message: str = "Logged out"
