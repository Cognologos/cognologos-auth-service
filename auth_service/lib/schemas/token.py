from .abc import BaseSchema


class TokenInfo(BaseSchema):
    access_token: str
    token_type: str = "Bearer"
