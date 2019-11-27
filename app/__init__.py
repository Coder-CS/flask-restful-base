from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config: object):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)