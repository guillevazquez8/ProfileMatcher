from app.campaign.db import create_campaign
from app.campaign.schema import CampaignSchema
from app.player.db import create_player
from flask import Blueprint, make_response
from app.player.schema import PlayerSchema
from sqlalchemy.exc import IntegrityError


init_bp = Blueprint("init_data", __name__, url_prefix="/init_data")


@init_bp.post("")
def init_data():
    """
    Initialize database with fresh data!
    ---
    tags:
        - Initialize data
    responses:
        201:
            description: Data successfully added to db!
    """
    try:
        player_data = {
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
                "name": "Hello world clan"
            },
            "_customfield": "mycustom"
        }
        player = PlayerSchema(**player_data)
        new_player = create_player(dict(player))

        campaign_data = {
            "game": "mygame",
            "name": "mycampaign",
            "priority": 10.5,
            "matchers": {
                "level": {
                    "min": 1,
                    "max": 3
                },
                "has": {
                    "country": ["US", "RO", "CA"],
                    "items": ["item_1"]
                },
                "does_not_have": {
                    "items": ["item_4"]
                }
            },
            "start_date": "2022-01-25 00:00:00Z",
            "end_date": "2022-02-25 00:00:00Z",
            "enabled": True,
            "last_updated": "2021-07-13 11:46:58Z"
        }
        campaign = CampaignSchema(**campaign_data)
        new_campaign = create_campaign(dict(campaign))
    except IntegrityError as e:
        return make_response("Data is already in the db", 409)

    return make_response({
        "Data has been added to the db":
            {
                "Player": {
                    "id": new_player.id,
                    "player_id": new_player.player_id
                }, "Campaign": {
                    "id": new_campaign.id
                }
            }
    }, 201)
