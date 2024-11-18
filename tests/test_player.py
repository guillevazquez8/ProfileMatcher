
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
        assert resp.json['credential'] == player['credential']
        assert resp.json['created'] == player['created']
        assert resp.json['modified'] == player['modified']
        assert resp.json['last_session'] == player['last_session']
        assert resp.json['total_spent'] == player['total_spent']
        assert resp.json['total_refund'] == player['total_refund']
        assert resp.json['total_transactions'] == player['total_transactions']
        assert resp.json['active_campaigns'] == player['active_campaigns']
        assert resp.json['devices'][0]['carrier'] == player['devices'][0]['carrier']
        assert resp.json['devices'][0]['firmware'] == player['devices'][0]['firmware']
        assert resp.json['devices'][0]['model'] == player['devices'][0]['model']
        assert resp.json['level'] == player['level']
        assert resp.json['xp'] == player['xp']
        assert resp.json['total_playtime'] == player['total_playtime']
        assert resp.json['country'] == player['country']
        assert resp.json['language'] == player['language']
        assert resp.json['birthdate'] == player['birthdate']
        assert resp.json['gender'] == player['gender']
        assert resp.json['inventory'] == player['inventory']
        assert resp.json['clan']['name'] == player['clan']['name']
        assert resp.json['_customfield'] == player['_customfield']


    def test_get_player(self, client, create_player_and_campaign):
        id = create_player_and_campaign[0].id
        resp = client.get(f"/player/{id}", headers=client.headers)
        assert resp.status_code == 200


    def test_get_player_and_update_campaigns(self, client, create_player_and_campaign):

        player, campaign = create_player_and_campaign
        player_id = player.player_id

        resp = client.get(f"/player/get_client_config/{player_id}", headers=client.headers)

        assert resp.status_code == 200
        assert len(resp.json['active_campaigns']) == 1
        assert resp.json['active_campaigns'][0]['game'] == campaign.game
        assert resp.json['active_campaigns'][0]['name'] == campaign.name


    def test_get_players(self, client, create_player_and_campaign):
        resp = client.get("/player/all")
        assert resp.status_code == 200
        assert len(resp.json) == 1


    def test_update_player_device(self, client, create_player_and_campaign):

        data = {
            "devices": {
                "model": "xiaomi redmi note 11",
                "carrier": "orange",
                "firmware": "321"
            }
        }

        player_id = create_player_and_campaign[0].id

        resp = client.put(f"/player/{player_id}", json=data, headers=client.headers)

        assert resp.status_code == 200
        data['devices']['player_id'] = player_id
        data['devices']['id'] = 2
        assert data['devices'] in resp.json['devices']


    def test_update_player_clan(self, client, create_player_and_campaign):

        data = {
            "clan": {
                "name": "newclan"
            }
        }

        player_id = create_player_and_campaign[0].id

        resp = client.put(f"/player/{player_id}", json=data, headers=client.headers)

        assert resp.status_code == 200
        assert resp.json['clan']['name'] == data['clan']['name']


    def test_delete_player(self, client, create_player_and_campaign):
        id = create_player_and_campaign[0].id
        resp = client.delete(f"/player/{id}")
        assert resp.status_code == 200
