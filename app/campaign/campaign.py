from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY


class Campaign(db.Model):
    id = Column(Integer, primary_key=True)
    game = Column(String)
    name = Column(String)
    priority = Column(Float)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    enabled = Column(Boolean)
    last_updated = Column(DateTime)
    matchers = db.relationship('Matchers', back_populates="campaign")

class Matchers(db.Model):
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaign.id'), nullable=False)
    level_min = Column(Integer)
    level_max = Column(Integer)
    has_country = Column(ARRAY(String))
    has_items = Column(ARRAY(String))
    does_not_have_items = Column(ARRAY(String))
    campaign = db.relationship('Campaign', back_populates='matchers')

class Level(db.Model):
    id = Column(Integer, primary_key=True)
    matchers_id = Column(Integer, ForeignKey("matchers.id"), nullable=False)
    min = Column(Integer)
    max = Column(Integer)
    matchers = db.relationship('Matchers', back_populates='level')

class Has(db.Model):
    id = Column(Integer, primary_key=True)
    matchers_id = Column(Integer, ForeignKey("matchers.id"), nullable=False)
    country = Column(ARRAY(String))
    items = Column(ARRAY(String))
    matchers = db.relationship('Matchers', back_populates='has')

class DoesNotHave(db.Model):
    id = Column(Integer, primary_key=True)
    matchers_id = Column(Integer, ForeignKey("matchers.id"), nullable=False)
    items = Column(ARRAY(String))
    matchers = db.relationship('Matchers', back_populates='does_not_have')

    """
    {
  "game": "mygame",
  "name":"mycampaign",
  "priority": 10.5,
  "matchers": {
    "level": {
      "min": 1,
      "max": 3
    },
    "has": {
      "country": ["US","RO","CA"],
      "items": ["item_1"]
    },
    "does_not_have": {
      "items": ["item_4"]
    },
  },
  "start_date": "2022-01-25 00:00:00Z",
  "end_date": "2022-02-25 00:00:00Z",
  "enabled": true,
  "last_updated": "2021-07-13 11:46:58Z"
}
    """