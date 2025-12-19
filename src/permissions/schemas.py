from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class PermissionCreateSchema(BaseModel):
    name: str
    description: str


class PermissionDeleteSchema(BaseModel):
    name: str


class PermissionUpdateSchema(BaseModel):
    name: str
    description: str


class PermissionPaertialUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None


class PermissionResponseSchema(BaseModel):
    id: int
    name: str
    description: str

    model_config = SettingsConfigDict(from_attributes=True)


class AssignPermissionSchema(BaseModel):
    permission_name: str


class RevokePermissionSchema(BaseModel):
    permission_name: str
