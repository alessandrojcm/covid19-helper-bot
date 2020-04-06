import pytest
from click.testing import CliRunner

from app.models import Config


@pytest.fixture(scope="function")
def config():
    return Config(TESTING=True)


@pytest.mark.parametrize(
    "debug,expected",
    [(True, 0), pytest.param(False, 1, marks=[pytest.mark.xfail])],
    scope="function",
)
def test_cli_run(debug, expected, config: Config):
    from app.scripts.cli import run

    config.DEBUG = debug
    runner = CliRunner()
    result = runner.invoke(run, obj=dict(config))

    assert result.exit_code == expected
