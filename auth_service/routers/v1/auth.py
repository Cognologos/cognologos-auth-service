from fastapi import APIRouter

from auth_service.core.dependencies.fastapi import EncryptorDependency
from auth_service.lib.schemas.token import TokenInfo
from auth_service.lib.schemas.user import UserLoginSchema


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenInfo)
async def login_user(user: UserLoginSchema, encryptor: EncryptorDependency) -> TokenInfo:
    payload = encryptor.encode_jwt(user.username)
    return TokenInfo(access_token=payload)
