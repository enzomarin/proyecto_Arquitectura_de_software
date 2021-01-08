from persistence import connect_database
import pytest

@pytest.fixture
def database_name():
    return "slack"


def test_connect_database():
    db = connect_database("root", "")
    assert db  is not None

