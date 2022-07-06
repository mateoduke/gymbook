import os
import tempfile
import pytest
from flaskr import create_app, db


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix='.db')

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_path
    })
    with app.app_context():
        db.create_all()
        yield app
    os.close(db_fd)
    os.unlink(db_path)
    try:
        os.remove(db_path)
    except FileNotFoundError:
        pass


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
