'''
database and session layer
1. creat SQLAlchemy async engine + session factory
2. creat redis async connection pool
3. expose fastapi dependency for injection functions
'''

from colections.abc import AsyncGenerator
from tyrping import Annotated

import redis.asyncio as aioredis
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# Async engine
engine: AsyncEngine = create_async_engine(
    str(settings.DATABASE_URL),
    
    # Connection pool parameters
    pool_size=settings.DB_POOL_SIZE,           # Core pool size
    max_overflow=settings.DB_MAX_OVERFLOW,     # Overflow slots
    pool_timeout=settings.DB_POOL_TIMEOUT,     # Checkout timeout (s)
    pool_recycle=settings.DB_POOL_RECYCLE,     # Max connection age (s)
    pool_pre_ping=True,       

    # debug
    echo=settings.DEBUG,                       # Log SQL in debug mode
)

# Async session factory

AsyncSessionFactory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,   
    autoflush=False,     
)


# Redis - Asunc connection pool

redis_pool: aioredis.BlockingConnectionPool = aioredis.BlockingConnectionPool.from_url(
    str(settings.REDIS_URL),
    max_connections = settings.REDIS_MAX_CONNECTIONS,
    decode_responses = True,
    socket_connect_timeout = 5,
    socket_timeout = 5,
)

# fastapi dependency injection functions

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    '''
    database session dependency.
    
    usage:
    async def end[oint(db: Dbsession) -> ...:
        result = await db.excute(...)
    '''