from typing import Annotated

from fastapi import APIRouter, Depends

from auth_service.core.dependencies.fastapi import DatabaseDependency, EncryptorDependency
from auth_service.core.exceptions.user import UserUnauthorizedException
from auth_service.lib.db import user as users_db
from auth_service.lib.schemas.token import TokenInfo
from auth_service.lib.schemas.user import UserLoginSchema, UserSchema


router = APIRouter(prefix="/auth", tags=["auth"])


async def validate_user(
    db: DatabaseDependency,
    encryptor: EncryptorDependency,
    user_login: UserLoginSchema,
) -> UserSchema:
    if not (user := await users_db.get_user_by_username(db, username=user_login.username)):
        raise UserUnauthorizedException
    if encryptor.hash_password(user_login.password) != user.hashed_password:
        raise UserUnauthorizedException
    return user


@router.post("/login", response_model=TokenInfo)
async def login_user(
    user: Annotated[UserLoginSchema, Depends(validate_user)],
    encryptor: EncryptorDependency,
) -> TokenInfo:
    payload = encryptor.encode_jwt(user.username)
    return TokenInfo(access_token=payload)
