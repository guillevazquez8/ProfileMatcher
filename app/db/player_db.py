from app.models.player import Player, Device, Clan, Inventory
from app.app import db
import uuid


def create_player(player_data: dict):
    # create player
    new_player = Player(player_id=uuid.uuid1())
    for key, value in player_data.items():
        if hasattr(new_player, key):
            setattr(new_player, key, value)
    db.add(new_player)
    db.commit()
    # create clan
    if player_data['clan']:
        clan = Clan(name=player_data['clan']['name'])
        db.add(clan)
        db.commit()
        new_player.clan_id = clan.id
        db.commit()
    # create device
    for device in player_data['devices']:
        new_device = Device(
            player_id=new_player.id,
            model=device['model'],
            carrier=device['carrier'],
            firmware=device['firmware']
        )
        db.add(new_device)
        db.commit()
    # create inventory
    if player_data['inventory']:
        new_inventory = Inventory(
            player_id=new_player.id,
            cash=player_data['inventory']['cash'],
            coins=player_data['inventory']['coins'],
            items=player_data['inventory']['items']
        )
        db.add(new_inventory)
        db.commit()
    return new_player


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
    db.commit()
    return player


def delete_player(id: int):
    player = get_player(id)
    db.delete(player)
    db.commit()
    return player


def update_player_campaigns(id: int, campaign_id: int):
    player = get_player(id)
    active_campaigns = player.active_campaigns
    if campaign_id not in player.active_campaigns:
        active_campaigns.append(campaign_id)
    player.active_campaigns = active_campaigns
    db.session.commit()
    return player
