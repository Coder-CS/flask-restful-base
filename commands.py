import click
from app import create_app, db, config
from app.models import User


app = create_app(config)


@app.cli.command("init_db")
def init_db():
    db.create_all()
    click.echo(f"{True}")


@app.cli.command("add_user")
@click.argument("email")
@click.argument("name")
@click.argument("password")
def add_user(email, name, password):
    user = User(email, name, password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"{user.id, user.name}")
