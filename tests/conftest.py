import pytest
from app.app import create_app, db
from app.models.player import Player
from config import config_test
from app.db.campaign_db import create_campaign
from app.db.player_db import create_player
from app.schemas.player_schema import PlayerSchema
from app.schemas.campaign_schema import CampaignSchema


@pytest.fixture()
def app():
    app = create_app(config_test)
    yield app

@pytest.fixture()
def client(app, request):
    test_client = app.test_client()
    test_client.headers = {"Content-Type": "application/json"}
    app.app_context().push()
    db.drop_all()
    db.create_all()

    def tearDown():
        db.session.remove()
        db.drop_all()
        pass

    request.addfinalizer(tearDown)
    return test_client

@pytest.fixture()
def create_player_and_campaign():
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
    create_campaign(dict(campaign))
    return new_player
