from pydantic import ValidationError

from app.models.player import Player, Device, Clan
from app.app import db
import uuid


def create_player(player_data: dict):
    # create player
    try:
        player_data['player_id'] = uuid.uuid1()
        player_copy = player_data.copy()
        for k in ('devices', 'clan'):
            player_data.pop(k, None)
        new_player = Player(**player_data)
        db.session.add(new_player)
        db.session.commit()
        # create clan
        if player_copy['clan']:
            clan = Clan(name=player_copy['clan'].name)
            db.session.add(clan)
            db.session.commit()
            new_player.clan_id = clan.id
            db.session.commit()
        # create device
        for device in player_copy['devices']:
            new_device = Device(
                player_id=new_player.id,
                model=device.model,
                carrier=device.carrier,
                firmware=device.firmware
            )
            db.session.add(new_device)
            db.session.commit()
        return new_player
    except Exception as e:
        raise e


def get_player(id: int):
    player = Player.query.get(id)
    return player


def get_player_by_player_id(player_id: str):
    player = Player.query.filter_by(player_id=player_id).first()
    return player


def update_player(id: int, data: dict):
    player = get_player(id)
    for key, value in data.items():
        if hasattr(player, key):
            setattr(player, key, value)
    db.session.commit()
    return player


def delete_player(id: int):
    player = get_player(id)
    db.session.delete(player)
    db.session.commit()
    return player


def update_player_campaigns(id: int, campaign: dict):
    player = get_player(id)
    active_campaigns = player.active_campaigns
    if campaign not in player.active_campaigns:
        active_campaigns.append(campaign)
    player.active_campaigns = active_campaigns
    db.session.commit()
    return player
