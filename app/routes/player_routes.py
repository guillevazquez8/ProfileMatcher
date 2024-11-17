from flask import Blueprint, request
from app.db.player_db import *
from app.db.campaign_db import get_enabled_campaigns, get_campaign_matcher
from app.schemas.player_schema import PlayerSchema
from flask_pydantic import validate
from flasgger.utils import swag_from


player_bp = Blueprint("player", __name__, url_prefix="/player")


@player_bp.post("")
@validate()
@swag_from({'tags': ['Player'], 'responses': {201: {}}})
def add_player(player_data: PlayerSchema):
    player = create_player(dict(player_data))
    return player


@player_bp.get("/{id}")
@swag_from({'tags': ['Player'], 'responses': {200: {}}})
def get_player_by_id(id: int):
    player = get_player(id)
    return player


@player_bp.put("/{id}")
@swag_from({'tags': ['Player'], 'responses': {200: {}}})
def update_player_by_id(id: int):
    data = request.get_json()
    player = update_player(id, data)
    return player


@player_bp.delete("/{id}")
@swag_from({'tags': ['Player'], 'responses': {200: {}}})
def delete_player_by_id(id: int):
    player = delete_player(id)
    return player


@player_bp.get("/get_client_config/{player_id}")
@swag_from({'tags': ['Player'], 'responses': {200: {}}})
def get_player_and_update_campaigns(player_id: str):
    # 1. get player
    player = get_player_by_player_id(player_id)
    # 2. get running campaigns
    running_campaigns = get_enabled_campaigns()
    # 3. check if matchers match player info
    # compare matchers from all running campaigns with player info
    for campaign in running_campaigns:
        matcher = get_campaign_matcher(campaign.id)
        # matcher conditions
        conditions = [
            lambda p: matcher.level.min >= p.level <= matcher.level.max,
            lambda p: p.country in matcher.have.country,
            lambda p: all(item in p.inventory.items for item in matcher.have.items),
            lambda p: all(item not in p.inventory.items for item in matcher.not_have.items)
        ]
        # 4. if matches, update player active campaigns
        if all(condition(player) for condition in conditions):
            player = update_player_campaigns(player.id, campaign.id)
    return player