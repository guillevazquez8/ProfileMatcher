from flask import Blueprint, request
from flask_pydantic import validate
from app.db.campaign_db import *
from app.schemas.campaign_schema import CampaignSchema
from flasgger.utils import swag_from
from pydantic import TypeAdapter


campaign_bp = Blueprint("campaign", __name__, url_prefix="/campaign")


@campaign_bp.post("")
@validate()
@swag_from({'tags': ['Campaign'], 'responses': {201: {}}})
def add_campaign():
    campaign_data = request.get_json()
    # data validation
    validator = TypeAdapter(CampaignSchema)
    valid_campaign = validator.validate_python(campaign_data)
    campaign = create_campaign(dict(valid_campaign))
    return campaign


@campaign_bp.get("/{id}")
@swag_from({'tags': ['Campaign'], 'responses': {200: {}}})
def get_campaign_by_id(id: int):
    campaign = get_campaign(id)
    return campaign


@campaign_bp.get("/all")
@swag_from({'tags': ['Campaign'], 'responses': {200: {}}})
def get_campaigns():
    campaigns = get_all_campaigns()
    return campaigns


@campaign_bp.get("/enabled")
@swag_from({'tags': ['Campaign'], 'responses': {200: {}}})
def get_campaigns_by_enabled():
    enabled_campaigns = get_enabled_campaigns()
    return enabled_campaigns


@campaign_bp.put("/{id}")
@swag_from({'tags': ['Campaign'], 'responses': {200: {}}})
def update_campaign_by_id(id: int):
    data = request.get_json()
    campaign = update_campaign(id, data)
    return campaign


@campaign_bp.delete("/{id}")
@swag_from({'tags': ['Campaign'], 'responses': {200: {}}})
def delete_campaign_by_id(id: int):
    campaign = delete_campaign(id)
    return campaign
