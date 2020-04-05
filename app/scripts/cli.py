import sys

import click

from app.core import config


@click.group()
def cli():
    """COVID19 Whatsapp Bot CLI Helper"""
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
def run(port, host):
    """Runs the development server"""
    if not config.DEBUG and not config.TESTING:
        click.echo("Run from CLI cannot be used in production.", err=True)
        sys.exit(1)
    elif config.TESTING:
        sys.exit(0)

    from .server_runner import run_app
    from app import get_application

    return run_app(get_application(), port, host)
