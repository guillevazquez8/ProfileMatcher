import pytest
from app.app import create_app, db
from config import config_test


@pytest.fixture()
def app():
    app = create_app(config_test)
    yield app

@pytest.fixture()
def client(app, request):
    test_client = app.test_client()
    test_client.headers = {"Content-Type": "application/json"}
    app.app_context().push()
    db.drop_all()
    db.create_all()

    def tearDown():
        db.drop_all()

    request.addfinalizer(tearDown)
    return test_client