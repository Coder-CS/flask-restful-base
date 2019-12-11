import click
from flask import Flask
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from app import db
from app.models import User


def register_commands(app: Flask):
    app.cli.add_command(init_db)


@click.command("init_db")
@with_appcontext
def init_db():
    db.create_all()
    print(f"{True}")
