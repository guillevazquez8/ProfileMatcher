from app.app import db
from app.models.campaign import Campaign, Matchers, Has, DoesNotHave, Level
from sqlalchemy.exc import SQLAlchemyError


def create_campaign(campaign_data: dict):
    try:
        # 1. format campaign_data to create a campaign object
        campaign_copy = campaign_data.copy()
        campaign_data.pop('matchers')

        # 2. create new campaign
        new_campaign = Campaign(**campaign_data)
        db.session.add(new_campaign)
        db.session.flush()

        # 3. create matcher if not null
        if campaign_copy['matchers']:
            new_matchers = Matchers(campaign_id=new_campaign.id)
            db.session.add(new_matchers)
            db.session.flush()

            # 4. create level if not null
            if campaign_copy['matchers'].level:
                level = Level(
                    matchers_id=new_matchers.id,
                    max=campaign_copy['matchers'].level.max,
                    min=campaign_copy['matchers'].level.min
                )
                db.session.add(level)

            # 5. create has if not null
            if campaign_copy['matchers'].has:
                has = Has(
                    matchers_id=new_matchers.id,
                    country=campaign_copy['matchers'].has.country,
                    items=campaign_copy['matchers'].has.items
                )
                db.session.add(has)

            # 6. create does_not_have if not null
            if campaign_copy['matchers'].does_not_have:
                does_not_have = DoesNotHave(
                    matchers_id=new_matchers.id,
                    items=campaign_copy['matchers'].does_not_have.items
                )
                db.session.add(does_not_have)

        # 7. commit changes to db
        db.session.commit()
        return new_campaign
    except SQLAlchemyError as e:
        db.session.rollback()
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
    try:
        # 1. get campaign
        campaign = get_campaign(id)
        # 2. check fields in data and update campaign accordingly
        for key, value in data.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)
        # 3. commit changes to db
        db.session.commit()
        return campaign
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e


def delete_campaign(id: int):
    try:
        campaign = get_campaign(id)
        db.session.delete(campaign)
        db.session.commit()
        return campaign
    except SQLAlchemyError as e:
        db.session.rollback()
        raise e
