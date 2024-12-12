from fastapi import APIRouter

from auth_service.core.dependencies.fastapi import DatabaseDependency
from auth_service.lib.db import user as user_db
from auth_service.lib.schemas.user import UserCreateSchema, UserSchema


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserSchema)
async def create_user(db: DatabaseDependency, schema: UserCreateSchema):
    return await user_db.create_user(
        db,
        schema=schema,
    )


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(db: DatabaseDependency, user_id: int):
    return await user_db.get_user(db, user_id=user_id)
