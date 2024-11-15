from flask import Blueprint

player_bp = Blueprint("player", __name__, url_prefix="/player")


@player_bp.get("/{player_id}")
def get_player_by_id(player_id: int):
    player = get_player_by_id(player_id)
    return player
