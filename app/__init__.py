from flask import Flask
from flask.views import View
from flask_sqlalchemy import SQLAlchemy
from app.config import configs, DevelopmentConfig
from app.apis import views

db = SQLAlchemy()


def create_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(configs.get(config_name, DevelopmentConfig))

    db.init_app(app)
    # 注册 api
    register_api(app)

    return app


def register_api(app: Flask):
    for view in views:
        register_api(app, view, view.endpoint, view.url, view.pk, view.pk_type)


def register_api(app: Flask, view: View, endpoint: str, url: str, pk: str = 'id', pk_type: str = 'int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=['GET', ])
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    app.add_url_rule(f"{url}<{pk_type}:{pk}>", view_func=view_func, methods=['GET', 'PUT', 'DELETE'])
