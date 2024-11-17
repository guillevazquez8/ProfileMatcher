from flask import Blueprint, request, make_response
from flask_pydantic import validate
from app.db.campaign_db import *
from app.schemas.campaign_schema import CampaignSchema
from flasgger.utils import swag_from
from pydantic import TypeAdapter


campaign_bp = Blueprint("campaign", __name__, url_prefix="/campaign")


@campaign_bp.post("")
@validate()
@swag_from("app/swagger/campaign_schema.yaml")
@swag_from({
    'tags': ['Campaign'],
    'responses': {201: {}}
})
def add_campaign():
    campaign_data = request.get_json()
    # data validation
    validator = TypeAdapter(CampaignSchema)
    valid_campaign = validator.validate_python(campaign_data)
    campaign = create_campaign(dict(valid_campaign))
    return make_response(campaign.to_dict(), 201)


@campaign_bp.get("/<int:id>")
@swag_from({'tags': ['Campaign'], 'responses': {200: {}}})
def get_campaign_by_id(id: int):
    campaign = get_campaign(id)
    return make_response(campaign.to_dict())


@campaign_bp.get("/all")
@swag_from({'tags': ['Campaign'], 'responses': {200: {}}})
def get_campaigns():
    campaigns = get_all_campaigns()
    campaigns_json = [campaign.to_dict() for campaign in campaigns]
    return make_response(campaigns_json)


@campaign_bp.get("/enabled")
@swag_from({'tags': ['Campaign'], 'responses': {200: {}}})
def get_campaigns_by_enabled():
    enabled_campaigns = get_enabled_campaigns()
    enabled_campaigns_json = [campaign.to_dict() for campaign in enabled_campaigns]
    return make_response(enabled_campaigns_json)


@campaign_bp.put("/<int:id>")
@swag_from({'tags': ['Campaign'], 'responses': {200: {}}})
def update_campaign_by_id(id: int):
    data = request.get_json()
    campaign = update_campaign(id, data)
    return make_response(campaign.to_dict())


@campaign_bp.delete("/<int:id>")
@swag_from({'tags': ['Campaign'], 'responses': {200: {}}})
def delete_campaign_by_id(id: int):
    campaign = delete_campaign(id)
    return make_response(campaign.to_dict())
