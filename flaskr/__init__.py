from flaskr.err import InvalidUsage

__version__ = "0.1.1"

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flaskr.config import configs, setting
from flaskr.redis_db import RedisDB
from flaskr.response import error_response


config_name = setting.get("ENV", "dev")
config = configs.get(config_name)

redis_config = {
    "host": config.REDIS_HOST,
    "port": config.REDIS_PORT,
    "db": config.REDIS_POOL_DB,
    "password": config.REDIS_PASSWORD
}
redis_db = RedisDB(**redis_config)

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    # 注册 api
    register_api(app)

    return app


def register_api(app: Flask):
    from flaskr.apis import LoginApi, LogoutApi
    LoginApi.register_api(app)
    LogoutApi.register_api(app)

