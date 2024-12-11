from .abc import BaseSchema


class TokenInfo(BaseSchema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
