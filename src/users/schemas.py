from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class RoleAssignSchema(BaseModel):
    user_email: str
    role_name: str

class RoleResponseSchema(BaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}


class UserCreateSchema(BaseModel):
    email: str
    password: str
    full_name: str


class UserUpdateSchema(BaseModel):
    email: str
    full_name: str
    password: str


class UserPartialUpdateSchema(BaseModel):
    email: str | None = None
    full_name: str | None = None
    password: str | None = None


class UserResponseSchema(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    role: RoleResponseSchema

    model_config = SettingsConfigDict(from_attributes=True)
