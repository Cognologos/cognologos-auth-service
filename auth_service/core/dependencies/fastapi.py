from typing import Annotated, Any, AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from auth_service.core.config import AppConfig

from ..security import Encryptor
from . import constructors as app_depends


def db_session_maker_stub() -> sessionmaker[Any]:
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


def encryptor(config: Annotated[AppConfig, Depends(app_depends.app_config)]) -> Encryptor:
    return app_depends.encryptor(config)


DatabaseDependency = Annotated[AsyncSession, Depends(db_session)]
EncryptorDependency = Annotated[Encryptor, Depends(encryptor)]
