from app.app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSON


class Player(db.Model):
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
    devices = db.relationship('Device', uselist=False, back_populates='player')
    inventory = db.relationship('Inventory', uselist=False, back_populates='player')
    clan_id = Column(Integer, ForeignKey('clans.id', ondelete="SET NULL"))
    clan = db.relationship('Clan', back_populates='player')
    active_campaigns = db.relationship("Campaign")


class CampaignPlayer(db.Model):
    __tablename__ = "campaign_player"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)


class Device(db.Model):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    model = Column(String)
    carrier = Column(String)
    firmware = Column(String)
    player_id = Column(Integer, db.ForeignKey('players.id', ondelete="CASCADE"), nullable=False)
    player = db.relationship('Player', back_populates='devices')


class Inventory(db.Model):
    __tablename__ = 'inventories'

    id = Column(Integer, primary_key=True)
    cash = Column(Integer)
    coins = Column(Integer)
    items = Column(JSON)
    player_id = Column(Integer, ForeignKey('players.id', ondelete="CASCADE"), nullable=False)
    player = db.relationship('Player', back_populates='inventory')


class Clan(db.Model):
    __tablename__ = 'clans'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    players = db.relationship('Player', back_populates='clan')
