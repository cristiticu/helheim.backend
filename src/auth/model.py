from pydantic import UUID4, BaseModel


class UserTokenData(BaseModel, frozen=True):
    raw_token: str
    user_guid: UUID4


class RefreshTokenData(BaseModel, frozen=True):
    raw_token: str
    user_guid: UUID4
