from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.database.config import settings


engine = create_engine(
    url=settings.database_url_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)


async_engine = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=True
)


session_factory = sessionmaker(engine)
async_session_factory = async_sessionmaker(async_engine)
