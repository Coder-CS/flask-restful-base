
__version__ = "0.1.1"

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import configs, setting
from app.apis import UserApi
from app.redis_db import RedisDB

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


def create_app(conf) -> Flask:
    app = Flask(__name__)
    app.config.from_object(conf)

    db.init_app(app)
    # 注册 api
    register_api(app)

    return app


def register_api(app: Flask):
    UserApi.register(app)

