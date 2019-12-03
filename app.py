import click
from flask import jsonify

from flaskr import create_app, db, InvalidUsage, error_response
from flaskr.models import User

app = create_app()


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    return jsonify(error.to_dict())


@app.errorhandler(404)
def page_not_found(error):
    return error_response("无效的请求"), 404


@app.cli.command("init_db")
def init_db():
    db.create_all()
    click.echo(f"{True}")


@app.cli.command("add_user")
@click.argument("email")
@click.argument("name")
@click.argument("password")
def add_user(email, name, password=None):
    user = User(email, name, password or "666666")
    db.session.add(user)
    db.session.commit()
    click.echo(f"{user.id, user.name}")
