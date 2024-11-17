from app.app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_serializer import SerializerMixin


class Player(db.Model, SerializerMixin):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    player_id = Column(String, unique=True, nullable=False)
    credential = Column(String)
    created = Column(DateTime, default=datetime.now())
    modified = Column(DateTime, onupdate=datetime.now())
    last_session = Column(DateTime)
    total_spent = Column(Float)
    total_refund = Column(Float)
    total_transactions = Column(Integer)
    last_purchase = Column(DateTime)
    level = Column(Integer)
    xp = Column(Integer)
    total_playtime = Column(Integer)
    country = Column(String(2))
    language = Column(String)
    birthdate = Column(DateTime)
    gender = Column(String)
    _customfield = Column(String)
    devices = db.relationship('Device')
    inventory = db.relationship('Inventory', uselist=False)
    clan_id = Column(Integer, ForeignKey('clans.id', ondelete="SET NULL"))
    active_campaigns = db.relationship("Campaign", secondary='campaign_player')


class CampaignPlayer(db.Model, SerializerMixin):
    __tablename__ = "campaign_player"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)


class Device(db.Model, SerializerMixin):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    model = Column(String)
    carrier = Column(String)
    firmware = Column(String)
    player_id = Column(Integer, db.ForeignKey('players.id', ondelete="CASCADE"), nullable=False)


class Inventory(db.Model, SerializerMixin):
    __tablename__ = 'inventories'

    id = Column(Integer, primary_key=True)
    cash = Column(Integer)
    coins = Column(Integer)
    items = Column(JSON)
    player_id = Column(Integer, ForeignKey('players.id', ondelete="CASCADE"), nullable=False)


class Clan(db.Model, SerializerMixin):
    __tablename__ = 'clans'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    players = db.relationship('Player')
