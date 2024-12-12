from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, Header, Request
from redis.asyncio import ConnectionPool, Redis as AbstractRedis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from auth_service.core.config import AppConfig

from ..security import Encryptor
from . import constructors as app_depends


def db_session_maker_stub() -> sessionmaker[Any]:
    raise NotImplementedError


def app_config_stub() -> AppConfig:
    raise NotImplementedError


async def db_session(
    request: Request,
    maker: Annotated[sessionmaker[Any], Depends(db_session_maker_stub)],
) -> AsyncGenerator[AsyncSession, None]:
    generator = app_depends.db_session_autocommit(maker)
    session = await anext(generator)
    request.state.db = session

    yield session

    try:
        await anext(generator)
    except StopAsyncIteration:
        pass
    else:
        raise RuntimeError("Database session not closed (db dependency generator is not closed).")


def redis_conn_pool_stub() -> ConnectionPool:
    """Get Redis connection pool stub.

    Raises:
        NotImplementedError: This is a stub function and should be implemented.

    Returns:
        ConnectionPool: The Redis connection pool.
    """
    raise NotImplementedError


async def redis_conn(
    request: Request, conn_pool: Annotated[ConnectionPool, Depends(redis_conn_pool_stub)]
) -> AsyncGenerator[AbstractRedis, None]:
    """Get Redis connection.

    Args:
        request (Request): The FastAPI request object.
        conn_pool (ConnectionPool): The Redis connection pool.

    Yields:
        AsyncGenerator[AbstractRedis, None]: A Redis connection.
    """
    generator = app_depends.redis_conn(conn_pool)
    redis = await anext(generator)
    request.state.redis = redis

    yield redis

    try:
        await anext(generator)
    except StopAsyncIteration:
        pass
    else:
        raise RuntimeError("Redis session not closed (redis dependency generator is not closed).")


def encryptor(config: Annotated[AppConfig, Depends(app_depends.app_config)]) -> Encryptor:
    return app_depends.encryptor(config)


def get_client_host(request: Request) -> str:
    client = request.client
    return client.host if client else ""


ClientHostDependency = Annotated[str, Depends(get_client_host)]
UserAgentDependency = Annotated[str, Header()]
EncryptorDependency = Annotated[Encryptor, Depends(encryptor)]
DatabaseDependency = Annotated[AsyncSession, Depends(db_session)]
RedisDependency = Annotated[AbstractRedis, Depends(redis_conn)]
