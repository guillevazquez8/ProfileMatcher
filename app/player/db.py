from werkzeug.exceptions import NotFound

from app.player.model import Player, Device, Clan
from app.app import db
import uuid
from sqlalchemy.exc import SQLAlchemyError


def create_player(player_data: dict):
    try:
        # 1. generate random player id and format data
        player_data['player_id'] = uuid.uuid1()
        # copy player data into another dict to create player without devices and clan
        player_copy = player_data.copy()
        # pop devices and clan as they are instances of pydantic schema and not part of player table
        for k in ('devices', 'clan'):
            player_data.pop(k, None)

        # 2. create new player
        new_player = Player(**player_data)
        db.session.add(new_player)
        db.session.flush()

        # 2. create clan if not null
        if player_copy['clan']:
            new_clan = create_clan(player_copy['clan'].name)
            new_player.clan_id = new_clan.id

        # 3. create device if not null
        for device in player_copy['devices']:
            create_device(dict(device), new_player.id)

        # 4. commit all changes to db
        db.session.commit()
        return new_player
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e


def create_clan(name: str):
    new_clan = Clan(name=name)
    db.session.add(new_clan)
    db.session.flush()
    return new_clan


def create_device(device: dict, player_id: int):
    new_device = Device(
        player_id=player_id,
        model=device['model'],
        carrier=device['carrier'],
        firmware=device['firmware']
    )
    db.session.add(new_device)
    return new_device


def get_player(id: int):
    player = Player.query.get(id)
    if not player:
        raise NotFound
    return player


def get_all_players():
    all_players = Player.query.all()
    return all_players


def get_all_players_player_id():
    all_players = get_all_players()
    player_id_list = [{"player_id": player.player_id} for player in all_players]
    return player_id_list


def get_player_by_player_id(player_id: str):
    player = Player.query.filter_by(player_id=player_id).first()
    return player


def update_player(id: int, data: dict):
    try:
        # 1. get player
        player = get_player(id)
        if not player:
            raise NotFound

        # 2. delete null fields
        update_data = data.copy()
        for k in data:
            if not data[k]:
                update_data.pop(k)

        # 3. devices is nested, it needs to be created separatedly
        if 'devices' in update_data:
            update_data['devices']['player_id'] = id
            devices = update_data.pop('devices')
            new_device = Device(**devices)
            db.session.add(new_device)

        # 4. if clan, check if name exists, if it does add its id, if it does not create it
        if "clan" in update_data:
            clan_name = update_data.pop('clan')['name']
            clan = Clan.query.filter_by(name=clan_name).first()
            if not clan:
                clan = create_clan(clan_name)
            update_data['clan_id'] = clan.id

        if "inventory" in update_data and player.inventory:
            # if player has inventory, update with introduced fields
            player.inventory = update_data['inventory']

        # 5. check fields in data and update player accordingly
        for key, value in update_data.items():
            if hasattr(player, key):
                setattr(player, key, value)

        # 6. commit changes to db
        db.session.commit()
        return player
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e


def delete_player(id: int):
    try:
        player = get_player(id)
        if not player:
            raise NotFound
        db.session.delete(player)
        db.session.commit()
        return id
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e


def update_player_campaigns(id: int, campaign: dict):
    try:
        # 1. get player
        player = get_player(id)
        # 2. get player active campaigns
        active_campaigns = player.active_campaigns
        # 3. if this campaign is not yet part of player active campaigns, add it
        if campaign not in player.active_campaigns:
            active_campaigns.append(campaign)
        # 4. update player active campaigns and commit changes
        player.active_campaigns = active_campaigns
        db.session.commit()
        return player
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
