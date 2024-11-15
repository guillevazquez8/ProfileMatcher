from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY


class Player(db.Model):


    """
    {
  "player_id": "97983be2-98b7-11e7-90cf-082e5f28d836",
  "credential": "apple_credential",
  "created": "2021-01-10 13:37:17Z",
  "modified": "2021-01-23 13:37:17Z",
  "last_session": "2021-01-23 13:37:17Z",
  "total_spent": 400,
  "total_refund": 0,
  "total_transactions": 5,
  "last_purchase": "2021-01-22 13:37:17Z",
  "active_campaigns": [],
  "devices": [
    {
      "id": 1,
      "model": "apple iphone 11",
      "carrier": "vodafone",
      "firmware": "123"
    }
  ],
  "level": 3,
  "xp": 1000,
  "total_playtime": 144,
  "country": "CA",
  "language": "fr",
  "birthdate": "2000-01-10 13:37:17Z",
  "gender": "male",
  "inventory": {
    "cash": 123,
    "coins": 123,
    "item_1": 1,
    "item_34": 3,
    "item_55": 2
  },
  "clan": {
    "id": "123456",
    "name": "Hello world clan"
  },
  "_customfield": "mycustom"
}
    """