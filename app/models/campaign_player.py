from app import db
from sqlalchemy import Column, Integer, ForeignKey


class CampaignPlayer(db.Model):
    __tablename__ = "campaign_player"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id", ondelete="CASCADE"), nullable=False)
