from app.app import db
from app.campaign.model import Campaign, Matchers, Has, DoesNotHave, Level
from sqlalchemy.exc import SQLAlchemyError


def create_campaign(campaign_data: dict):
    try:
        # 1. format campaign_data
        # copy campaign data into another dict to create campaign without matchers
        campaign_copy = campaign_data.copy()
        # pop matchers as they are instances of pydantic schema and not part of campaign table
        campaign_data.pop('matchers')

        # 2. create new campaign
        new_campaign = Campaign(**campaign_data)
        db.session.add(new_campaign)
        db.session.flush()

        # 3. create matchers if not null
        if campaign_copy['matchers']:
            create_matchers(dict(campaign_copy['matchers']), new_campaign.id)

        # 4. commit changes to db
        db.session.commit()
        return new_campaign
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e


def create_matchers(matchers: dict, campaign_id: int):

    # create matchers with juts foreign key to campaign
    new_matchers = Matchers(campaign_id=campaign_id)
    db.session.add(new_matchers)
    db.session.flush()

    # create level if not null
    if matchers['level']:
        create_level(dict(matchers['level']), new_matchers.id)

    # create has if not null
    if matchers['has']:
        create_has(dict(matchers['has']), new_matchers.id)

    # create does_not_have if not null
    if matchers['does_not_have']:
        create_does_not_have(dict(matchers['does_not_have']), new_matchers.id)

    return new_matchers


def create_level(level: dict, matcher_id: int):
    level = Level(
        matchers_id=matcher_id,
        max=level['max'],
        min=level['min']
    )
    db.session.add(level)


def create_has(has: dict, matcher_id: int):
    has = Has(
        matchers_id=matcher_id,
        country=has['country'],
        items=has['items']
    )
    db.session.add(has)


def create_does_not_have(does_not_have: dict, matcher_id: int):
    does_not_have = DoesNotHave(
        matchers_id=matcher_id,
        items=does_not_have['items']
    )
    db.session.add(does_not_have)


def get_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    return campaign


def get_all_campaigns():
    all_campaigns = Campaign.query.all()
    return all_campaigns


def get_enabled_campaigns():
    enabled_campaigns = Campaign.query.filter_by(enabled=True).all()
    return enabled_campaigns


def get_campaign_matchers(campaign_id):
    campaign = get_campaign(campaign_id)
    return campaign.matchers


def update_campaign(id: int, data: dict):
    try:
        # 1. get campaign
        campaign = get_campaign(id)

        # 2. matchers is nested, it needs to be updated separatedly
        if 'matchers' in data:
            matchers = data.pop('matchers')
            if campaign.matchers:
                update_matchers(campaign, matchers)
            else:
                create_matchers(matchers, campaign.id)

        # 3. check fields in data and update campaign accordingly
        for key, value in data.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)

        # 4. commit changes to db
        db.session.commit()
        return campaign
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e


def update_matchers(campaign: Campaign, matchers: dict):
    if 'level' in matchers:
        # if this campaign already includes levels, update them, else, create them
        if campaign.matchers.level:
            for k, v in matchers['level'].items():
                setattr(campaign.matchers.level, k, v)
            db.session.add(campaign.matchers.level)
        else:
            create_level(matchers['level'], campaign.matchers.id)
    if 'has' in matchers:
        create_level(matchers['level'], campaign.matchers.id)
    if 'does_not_have' in matchers:
        create_level(matchers['level'], campaign.matchers.id)


def delete_campaign(id: int):
    try:
        campaign = get_campaign(id)
        db.session.delete(campaign)
        db.session.commit()
        return id
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
