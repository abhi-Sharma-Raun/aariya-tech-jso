from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from .config import settings
import ssl

'''
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED
'''

DATABASE_URL_USER = f"postgresql+asyncpg://{settings.database_role}:{settings.database_password}@{settings.database_host}-pooler.c-2.{settings.database_region}.aws.neon.tech/{settings.database_name}"
engine = create_async_engine(
    DATABASE_URL_USER,
    pool_size=3, 
    max_overflow=5,
    pool_pre_ping=True,
    pool_recycle=3000
)
print("created user engine")
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False 
)
class Base(AsyncAttrs, DeclarativeBase):
    pass
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()