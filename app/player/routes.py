from flask import Blueprint, request, make_response
from jinja2.lexer import newline_re

from app.player.db import *
from app.campaign.db import get_enabled_campaigns, get_campaign_matchers
from app.player.schema import PlayerSchema
from pydantic import TypeAdapter


player_bp = Blueprint("player", __name__, url_prefix="/player")


@player_bp.post("")
def add_player():
    """
    Create Player
    ---
    consumes:
      - application/json
    tags:
      - Player
    parameters:
      - in: body
        name: player
        schema:
          type: object
          properties:
            credential:
              type: string
            created:
              type: string
              format: date-time
            modified:
              type: string
              format: date-time
            last_session:
              type: string
              format: date-time
            total_spent:
              type: number
            total_refund:
              type: number
            total_transactions:
              type: integer
            last_purchase:
              type: string
              format: date-time
            level:
              type: integer
            xp:
              type: integer
            total_playtime:
              type: integer
            country:
              type: string
              maxLength: 2
            language:
              type: string
            birthdate:
              type: string
              format: date-time
            gender:
              type: string
            _customfield:
              type: string
            devices:
              type: array
              items:
                type: object
                properties:
                  model:
                    type: string
                  carrier:
                    type: string
                  firmware:
                    type: string
            inventory:
              type: object
              additionalProperties:
                type: integer
            clan:
              type: object
              properties:
                name:
                  type: string
            active_campaigns:
              type: array
              items:
                type: integer
    responses:
      201:
        description: Player created
    """
    player_data = request.get_json()

    # data validation
    validator = TypeAdapter(PlayerSchema)
    valid_player = validator.validate_python(player_data)
    valid_player_dict = dict(valid_player)
    valid_player_dict['_customfield'] = player_data['_customfield']

    player = create_player(valid_player_dict)
    return make_response(player.to_dict(), 201)


@player_bp.get("/<int:id>")
def get_player_by_id(id: int):
    """
    Get Player by id
    ---
    tags:
        - Player
    parameters:
        - in: path
          name: id
          type: integer
          required: true
    responses:
        200:
            description: Success
    """
    player = get_player(id)
    return make_response(player.to_dict())


@player_bp.get("/all")
def get_players():
    """
    Get all players
    ---
    tags:
        - Player
    responses:
        200:
            description: Success
    """
    players = get_all_players()
    players_json = [player.to_dict() for player in players]
    return make_response(players_json)


@player_bp.put("/<int:id>")
def update_player_by_id(id: int):
    """
    Update Player by id
    ---
    tags:
        - Player
    parameters:
        - in: path
          name: id
          type: integer
          required: true
        - in: body
          name: player
          schema:
            type: object
            properties:
              credential:
                type: string
              created:
                type: string
                format: date-time
              modified:
                type: string
                format: date-time
              last_session:
                type: string
                format: date-time
              total_spent:
                type: number
              total_refund:
                type: number
              total_transactions:
                type: integer
              last_purchase:
                type: string
                format: date-time
              level:
                type: integer
              xp:
                type: integer
              total_playtime:
                type: integer
              country:
                type: string
                maxLength: 2
              language:
                type: string
              birthdate:
                type: string
                format: date-time
              gender:
                type: string
              _customfield:
                type: string
              devices:
                type: array
                items:
                  type: object
                  properties:
                    model:
                      type: string
                    carrier:
                      type: string
                    firmware:
                      type: string
              inventory:
                type: object
                additionalProperties:
                  type: integer
              clan:
                type: object
                properties:
                  name:
                    type: string
              active_campaigns:
                type: array
                items:
                  type: integer
    responses:
        200:
            description: Success
    """
    data = request.get_json()
    player = update_player(id, data)
    return make_response(player.to_dict())


@player_bp.delete("/<int:id>")
def delete_player_by_id(id: int):
    """
    Delete Player by id
    ---
    tags:
        - Player
    parameters:
        - in: path
          name: id
          type: integer
          required: true
    responses:
        200:
            description: Success
    """
    id = delete_player(id)
    return make_response({"player_removed": id})


@player_bp.get("/get_client_config/<string:player_id>")
def get_player_and_update_campaigns(player_id: str):
    """
    Get Player by player_id and update player active campaigns
    ---
    tags:
        - Player
    parameters:
        - in: path
          name: player_id
          type: string
          required: true
    responses:
        200:
            description: Success
    """
    # 1. get player
    player = get_player_by_player_id(player_id)
    if not player:
        return make_response(f"Player with id {player_id} does not exist", 422)

    # 2. get running campaigns
    enabled_campaigns = get_enabled_campaigns()

    # 3. check if matchers match player info
    # compare matchers from all running campaigns with player info
    for campaign in enabled_campaigns:
        matchers = get_campaign_matchers(campaign.id)
        if matchers:
            # check matchers
            conditions = [
                lambda p: matchers.level is None or matchers.level.min is None or matchers.level.min <= p.level,
                lambda p: matchers.level is None or matchers.level.max is None or matchers.level.max >= p.level,
                lambda p: matchers.has is None or matchers.has.country is None or p.country in matchers.has.country,
                lambda p: matchers.has is None or matchers.has.items is None or all(item in p.inventory for item in matchers.has.items),
                lambda p: matchers.does_not_have is None or matchers.does_not_have.items is None or all(item not in p.inventory for item in matchers.does_not_have.items)
            ]

            # 4. if matches, update player active campaigns
            if all(condition(player) for condition in conditions):
                player = update_player_campaigns(player.id, campaign)
        else:
            # if matchers is null, campaign is available to all players
            player = update_player_campaigns(player.id, campaign)
    return make_response(player.to_dict())
