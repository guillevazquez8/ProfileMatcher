from flask import Blueprint, request, make_response
from app.db.player_db import *
from app.db.campaign_db import get_enabled_campaigns, get_campaign_matchers
from app.schemas.player_schema import PlayerSchema
from flask_pydantic import validate
from flasgger.utils import swag_from
from pydantic import TypeAdapter


player_bp = Blueprint("player", __name__, url_prefix="/player")


@player_bp.post("")
@validate()
@swag_from("app/swagger/player_schema.yaml")
@swag_from({
    'tags': ['Player'],
    'responses': {201: {}}
})
def add_player():
    player_data = request.get_json()

    # data validation
    validator = TypeAdapter(PlayerSchema)
    valid_player = validator.validate_python(player_data)

    player = create_player(dict(valid_player))
    return make_response(player.to_dict(), 201)


@player_bp.get("/<int:id>")
@swag_from({'tags': ['Player'], 'responses': {200: {}}})
def get_player_by_id(id: int):
    player = get_player(id)
    return make_response(player.to_dict())


@player_bp.put("/<int:id>")
@swag_from({'tags': ['Player'], 'responses': {200: {}}})
def update_player_by_id(id: int):
    data = request.get_json()
    player = update_player(id, data)
    return make_response(player.to_dict())


@player_bp.delete("/<int:id>")
@swag_from({'tags': ['Player'], 'responses': {200: {}}})
def delete_player_by_id(id: int):
    player = delete_player(id)
    return make_response(player.to_dict())


@player_bp.get("/get_client_config/<string:player_id>")
@swag_from({'tags': ['Player'], 'responses': {200: {}}})
def get_player_and_update_campaigns(player_id: str):

    # 1. get player
    player = get_player_by_player_id(player_id)

    # 2. get running campaigns
    enabled_campaigns = get_enabled_campaigns()

    # 3. check if matchers match player info
    # compare matchers from all running campaigns with player info
    for campaign in enabled_campaigns:
        matchers = get_campaign_matchers(campaign.id)
        # check matchers
        conditions = [
            lambda p: matchers.level.min <= p.level <= matchers.level.max,
            lambda p: p.country in matchers.has.country,
            lambda p: all(item in p.inventory for item in matchers.has.items),
            lambda p: all(item not in p.inventory for item in matchers.does_not_have.items)
        ]

        # 4. if matches, update player active campaigns
        if all(condition(player) for condition in conditions):
            player = update_player_campaigns(player.id, campaign)
    return make_response(player.to_dict())
