from sqlalchemy_serializer import SerializerMixin
from app.app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY


class Campaign(db.Model, SerializerMixin):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    game = Column(String, nullable=False)
    name = Column(String, nullable=False)
    priority = Column(Float, default=0.0)
    start_date = Column(DateTime, default=datetime.today())
    end_date = Column(DateTime, default=datetime.today())
    enabled = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    matchers = db.relationship('Matchers', uselist=False)


class Matchers(db.Model, SerializerMixin):
    __tablename__ = 'matchers'

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id', ondelete="CASCADE"), nullable=False)
    level = db.relationship("Level", uselist=False)
    has = db.relationship('Has', uselist=False)
    does_not_have = db.relationship('DoesNotHave', uselist=False)


class Level(db.Model, SerializerMixin):
    __tablename__ = "levels"

    id = Column(Integer, primary_key=True)
    min = Column(Integer)
    max = Column(Integer)
    matchers_id = Column(Integer, ForeignKey("matchers.id", ondelete="CASCADE"), nullable=False)


class Has(db.Model, SerializerMixin):
    __tablename__ = "has"

    id = Column(Integer, primary_key=True)
    country = Column(ARRAY(String(2)))
    items = Column(ARRAY(String))
    matchers_id = Column(Integer, ForeignKey("matchers.id", ondelete="CASCADE"), nullable=False)


class DoesNotHave(db.Model, SerializerMixin):
    __tablename__ = "does_not_have"

    id = Column(Integer, primary_key=True)
    items = Column(ARRAY(String))
    matchers_id = Column(Integer, ForeignKey("matchers.id", ondelete="CASCADE"), nullable=False)
