import json


class TestPlayer:

    def test_create_player(self, client):
        player = {}
        resp = client.post("/player", data=json.dumps(player))
        assert resp.status_code == 201