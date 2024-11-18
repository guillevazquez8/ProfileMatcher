from pydantic import BaseModel, StringConstraints, Field, field_validator
from typing import Optional, Annotated
from datetime import datetime
import re


class DeviceSchema(BaseModel):
    model: Optional[str] = None
    carrier: Optional[str] = None
    firmware: Optional[str] = None


class ClanSchema(BaseModel):
    name: str


class PlayerSchema(BaseModel):
    credential: Optional[str] = None
    created: Optional[datetime] = None
    modified: Optional[datetime] = None
    last_session: Optional[datetime] = None
    total_spent: Optional[float] = None
    total_refund: Optional[float] = None
    total_transactions: Optional[int] = None
    last_purchase: Optional[datetime] = None
    level: Optional[int] = None
    xp: Optional[int] = None
    total_playtime: Optional[int] = None
    country: Annotated[str, StringConstraints(max_length=2), Field(default=None)]
    language: Optional[str] = None
    birthdate: Optional[datetime] = None
    gender: Optional[str] = None
    _customfield: Optional[str] = None
    devices: Optional[list[DeviceSchema]] = []
    inventory: Optional[dict[str, int]] = {"coins": 0, "cash": 0}
    clan: Optional[ClanSchema] = None
    active_campaigns: Optional[list[int]] = []

    @field_validator('inventory')
    def validate_inventory_keys(cls, value, field):
        for k, v in value.items():
            if k not in ["coins", "cash"] and not re.match(r"^item_\d+$", k):
                raise ValueError(f"Invalid key: {k}")
            if not isinstance(v, int):
                raise TypeError(f"Invalid value type for key {k}: expected int, got {type(v).__name__}")
        return value
