from pydantic import BaseModel, StringConstraints
from typing import Optional, Annotated
from datetime import datetime


class HasSchema(BaseModel):
    country: Optional[list[Annotated[str, StringConstraints(max_length=2)]]] = []
    items: Optional[list[str]] = []


class DoesNotHaveSchema(BaseModel):
    items: Optional[list[str]] = []


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
