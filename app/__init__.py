from werkzeug.security import generate_password_hash

__version__ = "0.1.1"

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import configs, setting
from app.redis_db import RedisDB
from app.response import error_response


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
    from app.apis import register_apis
    register_apis(app)
    # 注册命令
    from app.commands import register_commands
    register_commands(app)
    # 注册错误处理
    from app.error_handlers import register_error_handlers
    register_error_handlers(app)

    return app




