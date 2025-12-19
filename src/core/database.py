from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings

async_engine = create_async_engine(
    url=settings.SQLITE_DSN, echo=False, pool_size=5, max_overflow=10
)

async_session_factory = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session():
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


async def test_db_connection():
    try:
        async with async_engine.connect() as conn:
            print("Database connection successful")
    except Exception as exc:
        print(f"Database connection failed: {exc}")


class Base(DeclarativeBase):
    pass
