from datetime import datetime
from typing import Mapping
from pydantic import UUID4, BaseModel, ConfigDict


class Account(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    guid: UUID4
    password: str
    username: str
    c_at: datetime

    def to_db_item(self):
        return self.model_dump(mode="json")

    def to_dto(self):
        return AccountDto.model_validate(self, from_attributes=True)

    @classmethod
    def from_db_item(cls, item: Mapping):
        return Account.model_validate(item)


class AccountDto(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    guid: UUID4
    username: str
    c_at: datetime


class CreateAccount(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    username: str
    password: str
