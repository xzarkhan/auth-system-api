from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class SQLARepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(self.model).order_by(self.model.id))
        return result.scalars().all()

    async def get(self, id: int):
        result = await self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str):
        result = await self.session.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalar_one_or_none()

    async def create(self, data: dict):
        new_object = self.model(**data)
        self.session.add(new_object)
        await self.session.flush()
        return new_object

    async def update(self, id: int, data: dict):
        updated_object = await self.session.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        return updated_object.scalar_one_or_none()

    async def delete(self, id: int):
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id).returning(self.model)
        )
        return result.scalar_one_or_none()
