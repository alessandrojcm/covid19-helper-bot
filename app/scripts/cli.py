import sys

import click
from click import Context

from app.core import config


@click.group()
@click.pass_context
def cli(ctx: Context):
    """COVID19 Whatsapp Bot CLI Helper"""
    ctx.obj = dict(config)
    pass


@cli.command()
@click.option(
    "--port",
    default=8000,
    help="Port on which the server will run",
    type=click.IntRange(0, 52000),
    show_default=True,
)
@click.option(
    "--host",
    default="localhost",
    help="Host on which the app will run",
    type=click.STRING,
)
@click.pass_obj
def run(obj: dict, port, host):
    """Runs the development server"""
    if not obj["DEBUG"] and not obj["TESTING"]:
        click.echo("Run from CLI cannot be used in production.", err=True)
        sys.exit(1)
    elif obj["TESTING"]:
        sys.exit(0)

    from .server_runner import run_app
    from app import get_application

    return run_app(get_application(), port, host)


@cli.command()
def generate_env():
    """Generates a file .env with the default configuration values for development"""
    from .generate_dev_env import generate_dev_env

    click.echo("Generating .env file ...")
    generate_dev_env()
    click.echo(".env file generated correctly.")
