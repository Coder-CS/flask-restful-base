import os
import sys
import tempfile
import pytest

sys.path.append(".")
from app import db, create_app
from app.config import TestConfig


@pytest.fixture()
def client():
    app = create_app(TestConfig)
    db_fd, tempdir = tempfile.mkstemp()
    app.config['DATABASE_URI'] = f"sqlite:///{os.path.join(tempdir, 'data-test.db')}"
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(tempdir)


def test_empty_db(client):
    """Start with a blank database."""

    assert b'' in client.get('/users/sfasfas').data
    assert b'sfasfas' in client.get('/users/').data
