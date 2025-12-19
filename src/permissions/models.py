from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import RolesPermissions
from src.core.database import Base


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

    roles: Mapped[list["Role"]] = relationship(
        "Role", secondary=RolesPermissions.__table__, back_populates="permissions"
    )
