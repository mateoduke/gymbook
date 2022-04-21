import os
import pytest

from flaskr import create_app

@pytest.fixture
def app():
    pass

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
