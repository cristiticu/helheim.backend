from datetime import datetime
from typing import Optional
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
    role: str
    c_at: datetime
    meta_type: str = Field(default="REALM_USER")

    def to_db_item(self):
        s_key = f"USER#{self.user_guid}"
        meta_type = "REALM_USER"

        return {
            "guid": str(self.guid),
            "s_key": s_key,
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


class CreateRealmPortal(BaseModel):
    name: str
    world_name: str
    password: str


class CloseRealmPortal(BaseModel):
    portal_guid: UUID4
    instance_id: str
    spot_request_id: str
