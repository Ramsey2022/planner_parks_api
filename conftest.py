import pytest
from app import app


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def postal_code():
    postal_code = {
        "postal_code": "97124",
    }
    return dict(postal_code)
