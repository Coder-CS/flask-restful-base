import os
import tempfile
import pytest
from app import create_app, db
from app.models import User
from app.config import TestConfig


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
            User.add("240@qq.com", "xg", "asf")
        yield client

    os.close(db_fd)
    os.unlink(tempdir)


def test_login_fail(client):
    # 账号或密码错误
    data = {
        'account': "account", 'password': 'asf'
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "用户名或密码错误"
    data = {
        'account': "240@qq.com", 'password': 'asf1'
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "用户名或密码错误"

    # 账号为空
    data = {
        "account": "", "password": ""
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "account 不能为空"
    data = {
        "password": ""
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "account 不能为空"

    # 密码为空
    data = {
        "account": "as", "password": ""
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "password 不能为空"
    data = {
        "account": "fasf"
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("msg") == "password 不能为空"


def test_login(client):
    """Start with a blank database."""
    # 登录
    account = '240@qq.com'
    data = {
        'account': account, 'password': 'asf'
    }
    rv = client.post("/api/login", json=data)
    data = rv.get_json()
    assert data.get("status") == "success"
    token = data.get("data").get("token")
    assert type(token) is str

    # 获取登录信息
    rv = client.get(f"/api/login/{token}")
    data = rv.json
    assert account == data.get("data").get("account")

    # 更新令牌
    rv = client.put(f"/api/login/{token}")
    data = rv.json
    new_token = data.get("data").get("token")
    assert token != new_token

    # 推出登录
    rv = client.delete(f"/api/logout/{new_token}")
    data = rv.json
    assert data.get("msg") == "退出登录"

