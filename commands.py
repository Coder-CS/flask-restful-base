from app.config import env
from app import create_app
import click

from app.err import InvalidUsage


app = create_app()


# @app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error: InvalidUsage):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response


@app.cli.command("create-db")
@click.argument("name")
def print_user(name):
    print(f"this is {name}")

