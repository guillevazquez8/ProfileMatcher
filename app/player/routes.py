from flask import Blueprint, request, make_response
from sqlalchemy.exc import IntegrityError
from app.player.db import *
from app.campaign.db import get_enabled_campaigns, get_campaign_matchers
from app.player.schema import PlayerSchema, PlayerUpdateSchema
from pydantic import TypeAdapter, ValidationError


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
              example: "ES"
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
              properties:
                cash:
                  type: integer
                coins:
                  type: integer
                item_1:
                  type: integer
              example: {"cash": 100, "coins": 100, "item_1": 1}
            clan:
              type: object
              properties:
                name:
                  type: string
                  example: myclan
            active_campaigns:
              type: array
              items:
                type: object
              example: []
    responses:
      201:
        description: Player created
    """
    try:
        player_data = request.get_json()

        # data validation
        validator = TypeAdapter(PlayerSchema)
        valid_player = validator.validate_python(player_data)
        valid_player_dict = dict(valid_player)
        valid_player_dict['_customfield'] = player_data['_customfield']

        player = create_player(valid_player_dict)
        return make_response(player.to_dict(), 201)
    except ValidationError as e:
        return make_response(f"Validation Error: {str(e)}", 400)
    except IntegrityError as e:
        return make_response(f"Integrity Error: {str(e)}", 409)
    except AttributeError as e:
        return make_response(f"Bad Request: {e}", 400)


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
    try:
        player = get_player(id)
        return make_response(player.to_dict())
    except NotFound:
        return make_response(f"Player with id {id} does not exist", 404)


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


@player_bp.get("/all_player_id")
def get_players_player_id():
    """
    Get player_id from all players
    ---
    tags:
        - Player
    responses:
        200:
            description: Success
    """
    players_id_list = get_all_players_player_id()
    return make_response(players_id_list)


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
                example: "ES"
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
                properties:
                  cash:
                    type: integer
                    example: 100
                  coins:
                    type: integer
                    example: 100
                  item_1:
                    type: integer
                    example: 100
              clan:
                type: object
                properties:
                  name:
                    type: string
              active_campaigns:
                type: array
                items:
                  type: integer
                example: []
    responses:
        200:
            description: Success
    """
    try:
        player_data = request.get_json()

        # data validation
        validator = TypeAdapter(PlayerUpdateSchema)
        valid_player_update = validator.validate_python(player_data)
        valid_player_dict = dict(valid_player_update)

        player = update_player(id, valid_player_dict)
        return make_response(player.to_dict())
    except NotFound:
        return make_response(f"Player with id {id} does not exist", 404)
    except ValidationError as e:
        return make_response(f"Validation Error: {str(e)}", 400)


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
    try:
        id = delete_player(id)
        return make_response({"player_removed": id})
    except NotFound:
        return make_response(f"Player with id {id} does not exist", 404)


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
        return make_response(f"Player with id {player_id} does not exist", 404)

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
