from app.app import db
from app.models.campaign import Campaign, Matchers, Has, DoesNotHave, Level


def create_campaign(campaign_data: dict):
    # create campaign
    new_campaign = Campaign(
        game=campaign_data['game'],
        name=campaign_data['name']
    )
    for key, value in campaign_data.items():
        if hasattr(new_campaign, key):
            setattr(new_campaign, key, value)
    db.add(new_campaign)
    db.commit()
    # create matcher
    if campaign_data['matchers']:
        matchers = Matchers(campaign_id=new_campaign.id)
        db.add(matchers)
        db.commit()
        # create level
        if campaign_data['matchers']['level']:
            level = Level(
                matchers_id=matchers.id,
                max=campaign_data['matchers']['level']['max'],
                min=campaign_data['matchers']['level']['min']
            )
            db.add(level)
            db.commit()
        # create has
        if campaign_data['matchers']['has']:
            has = Has(
                matchers_id=matchers.id,
                country=campaign_data['matchers']['has']['country'],
                items=campaign_data['matchers']['has']['items']
            )
            db.add(has)
            db.commit()
        # create does_not_have
        if campaign_data['matchers']['does_not_have']:
            does_not_have = DoesNotHave(
                matchers_id=matchers.id,
                items=campaign_data['matchers']['does_not_have']['items']
            )
            db.add(does_not_have)
            db.commit()
    return new_campaign


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
    campaign = get_campaign(id)
    for key, value in data.items():
        if hasattr(campaign, key):
            setattr(campaign, key, value)
    db.commit()
    return campaign


def delete_campaign(id: int):
    campaign = get_campaign(id)
    db.delete(campaign)
    db.commit()
    return campaign
