from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(
    "sqlite+aiosqlite:///backend/db.db",
    echo=True
)
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False
)


class Base(DeclarativeBase):
    pass


async def create_tables():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
