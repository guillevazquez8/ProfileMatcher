from app.app import db
from app.models.campaign import Campaign, Matchers, Has, DoesNotHave, Level


def create_campaign(campaign_data: dict):
    # create campaign
    try:
        campaign_copy = campaign_data.copy()
        campaign_data.pop('matchers')
        new_campaign = Campaign(**campaign_data)
        db.session.add(new_campaign)
        db.session.commit()
        # create matcher
        if campaign_copy['matchers']:
            matchers = Matchers(campaign_id=new_campaign.id)
            db.session.add(matchers)
            db.session.commit()
            # create level
            if campaign_copy['matchers'].level:
                level = Level(
                    matchers_id=matchers.id,
                    max=campaign_copy['matchers'].level.max,
                    min=campaign_copy['matchers'].level.min
                )
                db.session.add(level)
                db.session.commit()
            # create has
            if campaign_copy['matchers'].has:
                has = Has(
                    matchers_id=matchers.id,
                    country=campaign_copy['matchers'].has.country,
                    items=campaign_copy['matchers'].has.items
                )
                db.session.add(has)
                db.session.commit()
            # create does_not_have
            if campaign_copy['matchers'].does_not_have:
                does_not_have = DoesNotHave(
                    matchers_id=matchers.id,
                    items=campaign_copy['matchers'].does_not_have.items
                )
                db.session.add(does_not_have)
                db.session.commit()
        return new_campaign
    except Exception as e:
        raise e


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
