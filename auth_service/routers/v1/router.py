from fastapi import APIRouter

from . import auth


router = APIRouter(prefix="/v1")

for i in [
    auth.router,
]:
    router.include_router(i)
