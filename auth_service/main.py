from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from auth_service.core.config import AppConfig
from auth_service.core.dependencies import constructors as app_depends, fastapi as stubs
from auth_service.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    config = AppConfig.from_env()
    with contextmanager(app_depends.db_session_maker)(config.database.url) as maker:
        app.dependency_overrides[stubs.app_config_stub] = lambda: config
        app.dependency_overrides[stubs.db_session_maker_stub] = lambda: maker

        yield


app = FastAPI(
    lifespan=lifespan,
)

app.include_router(router)
