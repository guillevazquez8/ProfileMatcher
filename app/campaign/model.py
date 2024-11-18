from sqlalchemy_serializer import SerializerMixin
from app.app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from app.helpers import UTCDateTime


class Campaign(db.Model, SerializerMixin):
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    game = Column(String, nullable=False)
    name = Column(String, nullable=False)
    priority = Column(Float, default=0.0)
    start_date = Column(UTCDateTime, default=datetime.now())
    end_date = Column(UTCDateTime, default=datetime.now())
    enabled = Column(Boolean, default=False)
    last_updated = Column(UTCDateTime, onupdate=datetime.now())
    matchers = db.relationship("Matchers", uselist=False, cascade="all")


class Matchers(db.Model, SerializerMixin):
    __tablename__ = 'matchers'

    id = Column(Integer, primary_key=True)
    level = db.relationship("Level", uselist=False, cascade='all')
    has = db.relationship('Has', uselist=False, cascade='all')
    does_not_have = db.relationship('DoesNotHave', uselist=False, cascade='all')
    campaign_id = Column(Integer, ForeignKey('campaigns.id', ondelete="CASCADE"), nullable=False)


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
