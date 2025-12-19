import asyncio

from src.core.database import async_engine, Base, async_session_factory
from src.permissions.models import Permission
from src.users.models import Role, User
from src.core.security import hash_password


async def start_seed():
    print("Seed is started...")

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_factory() as session:
        async with session.begin():

            # Permissions
            permissions = {
                "products:read": "Просмотр продуктов",
                "products:create": "Просмотр продуктов",
                "supplies:read": "Просмотр поставок",
                "supplies:create": "Создание поставок",
                "supplies:update": "Редактирование поставок",
                "supplies:delete": "Удаление поставок",
                "supplies:full_access": "Полный доступ к поставкам",
                "permissions:read": "Просмотр прав",
                "permissions:create": "Создание прав",
                "permissions:update": "Редактирование прав",
                "permissions:delete": "Удаление прав",
                "permissions:assign": "Назначение прав",
                "permissions:revoke": "Обнуление прав",
                "permissions:full_access": "Полный доступ к правам",
                "users:full_access": "Полный доступ к пользователям",
            }
            permissions_objects = {}
            for name, description in permissions.items():
                permission = Permission(name=name, description=description)
                session.add(permission)
                permissions_objects[name] = permission

            # Roles
            admin_role = Role(name="admin", description="Администратор")
            manager_role = Role(name="manager", description="Менеджер")
            seller_role = Role(name="seller", description="Продавец")
            consumer_role = Role(name="consumer", description="Потребитель")

            session.add_all([admin_role, manager_role, seller_role, consumer_role])

            # Roles permissions
            admin_role.permissions.extend(
                [
                    permissions_objects["permissions:full_access"],
                    permissions_objects["users:full_access"],
                ]
            )
            manager_role.permissions.extend([
                permissions_objects["supplies:full_access"]
            ])
            seller_role.permissions.extend(
                [
                    permissions_objects["supplies:read"],
                    permissions_objects["products:create"],
                ]
            )
            consumer_role.permissions.extend([
                permissions_objects["products:read"]
            ])

            # Users
            users = [
                (
                    "admin@example.com",
                    hash_password("admin_password"),
                    "Иванов Иван Иванович",
                    admin_role,
                ),
                (
                    "seller@example.com",
                    hash_password("seller_password"),
                    "Артемов Артем Артемович",
                    seller_role,
                ),
                (
                    "manager@example.com",
                    hash_password("manager_password"),
                    "Георгиев Георгий Георгиевич",
                    manager_role,
                ),
                (
                    "consumer@example.com",
                    hash_password("consumer_password"),
                    "Дмитриев Дмитрий Дмитриевич",
                    consumer_role,
                ),
            ]
            for email, password, full_name, role in users:
                session.add(
                    User(
                        email=email,
                        hashed_password=password,
                        full_name=full_name,
                        role=role,
                    )
                )
    print("Seed is completed")


async def main():
    await start_seed()


if __name__ == "__main__":
    asyncio.run(main())
