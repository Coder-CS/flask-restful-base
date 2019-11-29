from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskr.config import configs, env
from flaskr.apis import UserApi
from flaskr.redis_db import RedisDB

config_name = env.get("ENV", "dev")
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
    UserApi.register(app, "users", "/users/", "id", "int")

