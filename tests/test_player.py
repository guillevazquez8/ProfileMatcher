
class TestPlayer:

    def test_create_player(self, client):
        player = {
            "credential": "apple_credential",
            "created": "2021-01-10 13:37:17Z",
            "modified": "2021-01-23 13:37:17Z",
            "last_session": "2021-01-23 13:37:17Z",
            "total_spent": 400,
            "total_refund": 0,
            "total_transactions": 5,
            "last_purchase": "2021-01-22 13:37:17Z",
            "active_campaigns": [],
            "devices": [
                {
                    "model": "apple iphone 11",
                    "carrier": "vodafone",
                    "firmware": "123"
                }
            ],
            "level": 3,
            "xp": 1000,
            "total_playtime": 144,
            "country": "CA",
            "language": "fr",
            "birthdate": "2000-01-10 13:37:17Z",
            "gender": "male",
            "inventory": {
                "cash": 123,
                "coins": 123,
                "item_1": 1,
                "item_34": 3,
                "item_55": 2
            },
            "clan": {
                "name": "Hello world clan"
            },
            "_customfield": "mycustom"
        }
        resp = client.post("/player", json=player, headers=client.headers)
        assert resp.status_code == 201

    def test_get_player(self, client, create_player_and_campaign):
        id = create_player_and_campaign.id
        resp = client.get(f"/player/{id}", headers=client.headers)
        assert resp.status_code == 200

    def test_get_player_and_update_campaigns(self, client, create_player_and_campaign):
        player_id = create_player_and_campaign.player_id
        resp = client.get(f"/player/get_client_config/{player_id}", headers=client.headers)
        assert resp.status_code == 200
        resp_json = resp.json
        assert resp_json