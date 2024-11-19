from pydantic import BaseModel, StringConstraints, field_validator
from typing import Optional, Annotated
from datetime import datetime
import re


class HasSchema(BaseModel):
    country: Optional[list[Annotated[str, StringConstraints(max_length=2)]]] = []
    items: Optional[list[str]] = []

    @field_validator('items')
    def validate_inventory_keys(cls, value, field):
        for item in value:
            if not re.match(r"^item_\d+$", item):
                raise ValueError(f"Invalid item in Matchers.Has: {item}. It must start with 'item_' and follow with a number")
        return value


class DoesNotHaveSchema(BaseModel):
    items: Optional[list[str]] = []

    @field_validator('items')
    def validate_inventory_keys(cls, value, field):
        for item in value:
            if not re.match(r"^item_\d+$", item):
                raise ValueError(f"Invalid item in Matchers.DoesNotHave: {item}. It must start with 'item_' and follow with a number")
        return value


class LevelSchema(BaseModel):
    max: Optional[int] = None
    min: Optional[int] = None


class MatchersSchema(BaseModel):
    level: Optional[LevelSchema] = None
    has: Optional[HasSchema] = None
    does_not_have: Optional[DoesNotHaveSchema] = None


class CampaignSchema(BaseModel):
    game: str
    name: str
    priority: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    enabled: Optional[bool] = None
    last_updated: Optional[datetime] = None
    matchers: Optional[MatchersSchema] = None


class CampaignUpdateSchema(BaseModel):
    game: Optional[str] = None
    name: Optional[str] = None
    priority: Optional[float] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    enabled: Optional[bool] = None
    matchers: Optional[MatchersSchema] = None
