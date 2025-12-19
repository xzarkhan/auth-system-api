from src.core.base_repository import SQLARepository
from src.permissions.models import Permission


class PermissionRepository(SQLARepository):
    model = Permission
