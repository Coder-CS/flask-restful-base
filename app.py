from app.config import config
from app import create_app
import click

app = create_app(config.get("ENV", "dev"))


@app.cli.command("print-user")
@click.argument("name")
def print_user(name):
    print(f"this is {name}")


if __name__ == '__main__':
    app.run()
