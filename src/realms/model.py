from datetime import datetime
from typing import Literal, Optional, Union
from pydantic import UUID4, BaseModel, ConfigDict, Field
from shared.utils import format_utc_datetime_string


class Realm(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    guid: UUID4
    name: str
    description: Optional[str]
    c_at: datetime
    meta_type: str = Field(default="REALM")

    def to_db_item(self):
        s_key = "REALM#DETAILS"
        meta_type = "REALM"

        return {
            "guid": str(self.guid),
            "s_key": s_key,
            "name": self.name,
            "description": self.description,
            "c_at": format_utc_datetime_string(self.c_at),
            "meta_type": meta_type,
        }

    @classmethod
    def from_db_item(cls, item: dict):
        return Realm.model_validate(item)


class RealmUser(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    guid: UUID4
    user_guid: UUID4
    username: str
    role: str
    c_at: datetime
    meta_type: str = Field(default="REALM_USER")

    def to_db_item(self):
        s_key = f"USER#{self.user_guid}"
        meta_type = "REALM_USER"

        return {
            "guid": str(self.guid),
            "s_key": s_key,
            "username": self.username,
            "user_guid": str(self.user_guid),
            "role": self.role,
            "c_at": format_utc_datetime_string(self.c_at),
            "meta_type": meta_type,
        }

    @classmethod
    def from_db_item(cls, item: dict):
        split_s_key = item["s_key"].split("#")
        item_payload = {
            **item,
            "user_guid": split_s_key[1],
        }
        return RealmUser.model_validate(item_payload)


class RealmPortal(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    guid: UUID4
    portal_guid: UUID4
    opened_by_user_guid: UUID4
    instance_id: str
    spot_request_id: str
    password: str
    name: str
    world_name: str
    public_address: str
    region: str
    instance_type: str
    status: str
    c_at: datetime
    meta_type: str = Field(default="REALM_PORTAL")

    def to_db_item(self):
        s_key = f"PORTAL#{self.portal_guid}"
        meta_type = "REALM_PORTAL"

        return {
            "guid": str(self.guid),
            "opened_by_user_guid": str(self.opened_by_user_guid),
            "s_key": s_key,
            "instance_id": self.instance_id,
            "spot_request_id": self.spot_request_id,
            "name": self.name,
            "world_name": self.world_name,
            "password": self.password,
            "public_address": self.public_address,
            "region": self.region,
            "instance_type": self.instance_type,
            "status": self.status,
            "c_at": format_utc_datetime_string(self.c_at),
            "meta_type": meta_type,
        }

    @classmethod
    def from_db_item(cls, item: dict):
        split_s_key = item["s_key"].split("#")
        item_payload = {
            **item,
            "portal_guid": split_s_key[1],
        }
        return RealmPortal.model_validate(item_payload)


class RealmWorld(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    name: str
    m_at: datetime

    def to_db_item(self):
        return {
            "name": self.name,
            "m_at": format_utc_datetime_string(self.m_at),
        }

    @classmethod
    def from_db_item(cls, item: dict):
        return RealmWorld.model_validate(item)


class RealmListFile(BaseModel):
    model_config = ConfigDict(revalidate_instances='always')

    file_name: str
    content: str

    def to_db_item(self):
        return {
            "file_name": self.file_name,
            "content": self.content,
        }

    @classmethod
    def from_db_item(cls, item: dict):
        return RealmListFile.model_validate(item)


class CloseRealmPortal(BaseModel):
    portal_guid: UUID4
    instance_id: str
    spot_request_id: str


class CreateRealmWorldBackup(BaseModel):
    backup_name: str


class CreateRealmFile(BaseModel):
    file_name: str
    content: str


class CombatModifier(BaseModel):
    key: Literal["combat"]
    value: Literal["normal", "veryeasy", "easy", "hard", "veryhard"]


class DeathPenaltyModifier(BaseModel):
    key: Literal["deathpenalty"]
    value: Literal["normal", "casual", "veryeasy", "easy", "hard", "hardcore"]


class ResourcesModifier(BaseModel):
    key: Literal["resources"]
    value: Literal["normal", "muchless", "less", "more", "muchmore", "most"]


class RaidsModifier(BaseModel):
    key: Literal["raids"]
    value: Literal["normal", "none", "muchless", "less", "more", "muchmore"]


class PortalsModifier(BaseModel):
    key: Literal["portals"]
    value: Literal["normal", "casual", "hard", "veryhard"]


WorldModifier = Union[
    CombatModifier,
    DeathPenaltyModifier,
    ResourcesModifier,
    RaidsModifier,
    PortalsModifier,
]


class CreateRealmPortal(BaseModel):
    name: str
    world_name: str
    password: str
    preset: Optional[Literal["normal", "casual", "easy",
                             "hard", "hardcore", "immersive", "hammer"]] = None
    modifiers: Optional[list[WorldModifier]] = None
    keys: Optional[list[Literal["nobuildcost",
                                "playerevents", "passivemobs", "nomap"]]] = None
