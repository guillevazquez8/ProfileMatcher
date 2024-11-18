
class TestCampaign:


    def test_create_campaign(self, client):

        campaign = {
            "game": "mygame",
            "name":"mycampaign",
            "priority": 10.5,
            "matchers": {
                "level": {
                "min": 1,
                "max": 3
                },
                "has": {
                    "country": ["US","RO","CA"],
                    "items": ["item_1"]
                },
                "does_not_have": {
                    "items": ["item_4"]
                }
            },
            "start_date": "2022-01-25 00:00:00Z",
            "end_date": "2022-02-25 00:00:00Z",
            "enabled": True,
            "last_updated": "2021-07-13 11:46:58Z"
        }

        resp = client.post("/campaign", json=campaign, headers=client.headers)

        assert resp.status_code == 201
        assert resp.json['game'] == campaign['game']
        assert resp.json['name'] == campaign['name']
        assert resp.json['priority'] == campaign['priority']
        assert resp.json['matchers']['level']['max'] == campaign['matchers']['level']['max']
        assert resp.json['matchers']['level']['min'] == campaign['matchers']['level']['min']
        assert resp.json['matchers']['has']['country'] == campaign['matchers']['has']['country']
        assert resp.json['matchers']['has']['items'] == campaign['matchers']['has']['items']
        assert resp.json['matchers']['does_not_have']['items'] == campaign['matchers']['does_not_have']['items']
        assert resp.json['start_date'] == campaign['start_date']
        assert resp.json['end_date'] == campaign['end_date']
        assert resp.json['enabled'] == campaign['enabled']
        assert resp.json['last_updated'] == campaign['last_updated']


    def test_get_campaign(self, client, create_player_and_campaign):
        id = create_player_and_campaign[1].id
        resp = client.get(f"/campaign/{id}", headers=client.headers)
        assert resp.status_code == 200


    def test_get_all_campaigns(self, client, create_player_and_campaign):
        resp = client.get("/campaign/all")
        assert resp.status_code == 200
        assert len(resp.json) == 1


    def test_get_enabled_campaigns(self, client, create_player_and_campaign):
        resp = client.get("/campaign/enabled")
        assert resp.status_code == 200
        assert len(resp.json) == 1


    def test_update_campaign_matchers(self, client, create_player_and_campaign):

        data = {
            "matchers": {
                "level": {
                    "min": 2,
                    "max": 5
                }
            }
        }

        id = create_player_and_campaign[1].id

        resp = client.put(f"/campaign/{id}", json=data, headers=client.headers)

        assert resp.status_code == 200
        assert resp.json['matchers']['level']['min'] == data['matchers']['level']['min']
        assert resp.json['matchers']['level']['max'] == data['matchers']['level']['max']


    def test_delete_campaign(self, client, create_player_and_campaign):
        id = create_player_and_campaign[1].id
        resp = client.delete(f"/campaign/{id}")
        assert resp.status_code == 200