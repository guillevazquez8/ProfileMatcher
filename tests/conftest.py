import pytest
from app.app import create_app, db


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": 'postgresql://guille:celta@localhost:5432/profile_matcher_test'
    })
    yield app

@pytest.fixture()
def client(app, request):
    test_client = app.test_client()
    app.app_context().push()
    db.drop_all()
    db.create_all()

    def tearDown():
        db.drop_all()

    request.addfinalizer(tearDown)
    return test_client