import pytest
from click.testing import CliRunner
from starlette.config import environ

# Secret Key is needed
environ["SECRET_KEY"] = "123"
environ["TESTING"] = "True"


@pytest.mark.parametrize(
    "debug,expected",
    [("True", 0), pytest.param("False", 1, marks=[pytest.mark.xfail])],
    scope="function",
)
def test_cli_run(debug, expected):
    environ["DEBUG"] = debug
    from app.scripts import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["run"])

    assert result.exit_code == expected
