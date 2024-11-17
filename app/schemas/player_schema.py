from pydantic import BaseModel, StringConstraints, Field
from typing import Optional, Annotated
from datetime import datetime


class DeviceSchema(BaseModel):
    model: Optional[str] = None
    carrier: Optional[str] = None
    firmware: Optional[str] = None

class InventorySchema(BaseModel):
    cash: Optional[int] = None
    coins: Optional[int] = None
    items: Optional[dict] = None

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
    inventory: Optional[InventorySchema] = None
    clan: Optional[ClanSchema] = None
    active_campaigns: Optional[list[int]] = []

