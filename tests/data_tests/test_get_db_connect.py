from unittest.mock import patch, MagicMock

import pytest
from sqlalchemy.engine import Engine

from src.air_quality.data.get_db_connect import get_db_connect


# Patch create_engine from sqlalchemy
@patch("src.air_quality.data.get_db_connect.create_engine")
def test_get_db_connect_returns_engine(mock_create_engine):
    """Verifies that function returns a SQLalchemy engine object."""
    # Mock return value from create_engine
    mock_engine = MagicMock(spec=Engine)
    mock_create_engine.return_value = mock_engine
    # Call function with test parameters
    engine = get_db_connect("user", "password", "localhost", "5432", "dbname")
    # Verify that create_engine was called
    mock_create_engine.assert_called_once()
    # Assert that function returns an engine object
    assert isinstance(engine, Engine)


@patch("src.air_quality.data.get_db_connect.create_engine")
def test_get_db_connect_correct_url(mock_create_engine):
    """Verifies the function constructs the correct database URL."""
    # Call function with test parameters
    get_db_connect("user", "password", "localhost", "5432", "dbname")
    # Assert that create_engine was called with correct url
    expected_url = "postgresql://user:password@localhost:5432/dbname"
    mock_create_engine.assert_called_once_with(url=expected_url)


def test_get_db_connect_invalid_inputs():
    """Tests if function raises proper error when receiving invalid inputs."""
    # Invalid username
    with pytest.raises(ValueError):
        get_db_connect("", "password", "localhost", "5432", "dbname")
    # Invalid password
    with pytest.raises(ValueError):
        get_db_connect("user", "", "localhost", "5432", "dbname")
    # Invalid host
    with pytest.raises(ValueError):
        get_db_connect("user", "password", "", "5432", "dbname")
    # Invalid port
    with pytest.raises(ValueError):
        get_db_connect("user", "password", "localhost", "", "dbname")
    # Invalid database name
    with pytest.raises(ValueError):
        get_db_connect("user", "password", "localhost", "5432", "")
