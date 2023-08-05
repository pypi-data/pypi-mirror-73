import pytest
from click.testing import CliRunner
from flight_optimizer.cli import search


@pytest.fixture(scope='module')
def runner():
    return CliRunner()


def test_search(runner):
    response = runner.invoke(search, [])
    assert response.exit_code == 0
    assert response.output == ""
