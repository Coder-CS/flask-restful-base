import click
from app import create_app, db, app
from app.models import User


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
