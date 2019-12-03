import json
import os
import sys
import tempfile

from flask_sqlalchemy import SQLAlchemy
import pytest

sys.path.append(".")
from flaskr import create_app, db
from flaskr.models import User
from flaskr.config import TestConfig



@pytest.fixture()
def client():

    db_fd, tempdir = tempfile.mkstemp()
    TestConfig.SQLALCHEMY_DATABASE_URI = f"sqlite:///{tempdir}"
    app = create_app()
    app.config.from_object(TestConfig)
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            user = User("240@qq.com", "xg", "asf")
            db.session.add(user)
            db.session.commit()
        yield client

    os.close(db_fd)
    os.unlink(tempdir)


def test_login_fail(client):
    data = {
        'email': "email", 'password': 'asf'
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "用户名或密码错误"
    data = {
        'email': "240@qq.com", 'password': 'asf1'
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "用户名或密码错误"
    data = {
        "email": "", "password": ""
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "email 不能为空"
    data = {
        "password": ""
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "email 不能为空"
    data = {
        "email": "as", "password": ""
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "password 不能为空"
    data = {
        "email": "fasf"
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "password 不能为空"


def test_login(client):
    """Start with a blank database."""
    email = '240@qq.com'
    data = {
        'email': email, 'password': 'asf'
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("status") == "success"
    token = data.get("data").get("token")
    assert type(token) is str
    rv = client.get(f"/api/login/{token}")
    data = rv.json
    assert email == data.get("data").get("email")
    rv = client.delete(f"/api/logout/{token}12")
    data = rv.json
    assert data.get("msg") == "无效的令牌"
    rv = client.put(f"/api/login/{token}")
    data = rv.json
    assert token != data.get("data").get("token")
    rv = client.delete(f"/api/logout/{token}")
    data = rv.json
    assert data.get("msg") == "退出登录"

