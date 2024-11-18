from flask import Blueprint, request, make_response
from sqlalchemy.exc import IntegrityError
from app.campaign.db import *
from app.campaign.schema import CampaignSchema
from pydantic import TypeAdapter, ValidationError


campaign_bp = Blueprint("campaign", __name__, url_prefix="/campaign")


@campaign_bp.post("")
def add_campaign():
    """
    Create Campaign
    ---
    consumes:
      - application/json
    tags:
      - Campaign
    parameters:
      - in: body
        name: campaign
        required: true
        schema:
          type: object
          required:
            - game
            - name
          properties:
            game:
              type: string
            name:
              type: string
            priority:
              type: number
            start_date:
              type: string
              format: date-time
            end_date:
              type: string
              format: date-time
            enabled:
              type: boolean
            last_updated:
              type: string
              format: date-time
            matchers:
              type: object
              properties:
                level:
                  type: object
                  properties:
                    max:
                      type: integer
                    min:
                      type: integer
                has:
                  type: object
                  properties:
                    country:
                      type: array
                      items:
                        type: string
                        maxLength: 2
                    items:
                      type: array
                      items:
                        type: string
                does_not_have:
                  type: object
                  properties:
                    items:
                      type: array
                      items:
                        type: string
    responses:
      201:
        description: Campaign created
    """
    try:
        campaign_data = request.get_json()
        # data validation
        validator = TypeAdapter(CampaignSchema)
        valid_campaign = validator.validate_python(campaign_data)

        campaign = create_campaign(dict(valid_campaign))
        return make_response(campaign.to_dict(), 201)
    except ValidationError as e:
        return make_response(f"Validation Error: {str(e)}", 400)
    except IntegrityError as e:
        return make_response(f"Integrity Error: {str(e)}", 409)
    except AttributeError as e:
        return make_response(f"Bad Request: {e}", 400)


@campaign_bp.get("/<int:id>")
def get_campaign_by_id(id: int):
    """
    Get Campaign by id
    ---
    tags:
        - Campaign
    parameters:
        - in: path
          name: id
          type: integer
          required: true
    responses:
        200:
            description: Success
    """
    campaign = get_campaign(id)
    return make_response(campaign.to_dict())


@campaign_bp.get("/all")
def get_campaigns():
    """
    Get all campaigns
    ---
    tags:
        - Campaign
    responses:
        200:
            description: Success
    """
    campaigns = get_all_campaigns()
    campaigns_json = [campaign.to_dict() for campaign in campaigns]
    return make_response(campaigns_json)


@campaign_bp.get("/enabled")
def get_campaigns_by_enabled():
    """
    Get all enabled campaigns
    ---
    tags:
        - Campaign
    responses:
        200:
            description: Success
    """
    enabled_campaigns = get_enabled_campaigns()
    enabled_campaigns_json = [campaign.to_dict() for campaign in enabled_campaigns]
    return make_response(enabled_campaigns_json)


@campaign_bp.put("/<int:id>")
def update_campaign_by_id(id: int):
    """
    Update Campaign by id
    ---
    tags:
        - Campaign
    parameters:
        - in: path
          name: id
          type: integer
          required: true
        - in: body
          name: campaign
          required: true
          schema:
            type: object
            properties:
              game:
                type: string
              name:
                type: string
              priority:
                type: number
              start_date:
                type: string
                format: date-time
              end_date:
                type: string
                format: date-time
              enabled:
                type: boolean
              last_updated:
                type: string
                format: date-time
              matchers:
                type: object
                properties:
                  level:
                    type: object
                    properties:
                      max:
                        type: integer
                      min:
                        type: integer
                  has:
                    type: object
                    properties:
                      country:
                        type: array
                        items:
                          type: string
                          maxLength: 2
                      items:
                        type: array
                        items:
                          type: string
                  does_not_have:
                    type: object
                    properties:
                      items:
                        type: array
                        items:
                          type: string
    responses:
        200:
            description: Success
    """
    data = request.get_json()
    campaign = update_campaign(id, data)
    return make_response(campaign.to_dict())


@campaign_bp.delete("/<int:id>")
def delete_campaign_by_id(id: int):
    """
    Delete Campaign by id
    ---
    tags:
        - Campaign
    parameters:
        - in: path
          name: id
          type: integer
          required: true
    responses:
        200:
            description: Success
    """
    id = delete_campaign(id)
    return make_response({"campaign_removed": id})
