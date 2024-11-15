from app.models.player import Player


def get_player_by_id(player_id: int):
    player = Player.query.filter_by(player_id=player_id)
    return player