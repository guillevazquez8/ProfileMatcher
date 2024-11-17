from app.app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY


class Campaign(db.Model):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    game = Column(String, nullable=False)
    name = Column(String, nullable=False)
    priority = Column(Float, default=0.0)
    start_date = Column(DateTime, default=datetime.today())
    end_date = Column(DateTime, default=datetime.today())
    enabled = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    matcher = db.relationship('Matchers', uselist=False, back_populates="campaign")


class Matchers(db.Model):
    __tablename__ = 'matchers'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id', ondelete="CASCADE"), nullable=False)
    campaign = db.relationship('Campaign', back_populates='matchers')
    level = db.relationship("Level", uselist=False, back_populates="matchers")
    have = db.relationship('Has', uselist=False, back_populates='matchers')
    not_have = db.relationship('DoesNotHave', uselist=False, back_populates='matchers')


class Level(db.Model):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    min = Column(Integer)
    max = Column(Integer)
    matchers_id = Column(Integer, ForeignKey("matchers.id", ondelete="CASCADE"), nullable=False)
    matchers = db.relationship('Matchers', back_populates='has')


class Has(db.Model):
    __tablename__ = "has"

    id = Column(Integer, primary_key=True)
    country = Column(ARRAY(String(2)))
    items = Column(ARRAY(String))
    matchers_id = Column(Integer, ForeignKey("matchers.id", ondelete="CASCADE"), nullable=False)
    matchers = db.relationship('Matchers', back_populates='has')


class DoesNotHave(db.Model):
    __tablename__ = "does_not_have"

    id = Column(Integer, primary_key=True)
    items = Column(ARRAY(String))
    matchers_id = Column(Integer, ForeignKey("matchers.id", ondelete="CASCADE"), nullable=False)
    matchers = db.relationship('Matchers', back_populates='does_not_have')
