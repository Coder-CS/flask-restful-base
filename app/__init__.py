from app.err import InvalidUsage

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
    register_api(app)

    return app


def register_api(app: Flask):
    from app.apis import LoginApi, LogoutApi
    LoginApi.register_api(app)
    LogoutApi.register_api(app)


app = create_app()


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return jsonify(error.to_dict())


@app.errorhandler(404)
def page_not_found(error):
    return error_response("无效的请求"), 404
