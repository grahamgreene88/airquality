from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
from pandas import Timestamp
from pandas.testing import assert_frame_equal
from sqlalchemy.exc import OperationalError

from src.air_quality.data.get_db_connect import get_db_connect
from src.air_quality.data.get_db_data import get_db_data

# Mock expected data to be returned from SQL query
mock_query_result = pd.DataFrame(
    {
        "datetime": [
            Timestamp("2024-05-31 18:00:00+0000", tz="UTC"),
            Timestamp("2024-05-31 18:00:00+0000", tz="UTC"),
            Timestamp("2024-05-31 18:00:00+0000", tz="UTC"),
            Timestamp("2024-05-31 17:00:00+0000", tz="UTC"),
            Timestamp("2024-05-31 17:00:00+0000", tz="UTC"),
            Timestamp("2024-05-31 17:00:00+0000", tz="UTC"),
        ],
        "parameter": [
            "Particulate matter (PM2.5)",
            "Ozone (O3)",
            "Nitrogen dioxide (NO2)",
            "Particulate matter (PM2.5)",
            "Nitrogen dioxide (NO2)",
            "Ozone (O3)",
        ],
        "value": [4.0, 43.0, 0.0, 4.0, 0.0, 43.0],
        "unit": ["µg/m³", "ppb", "ppb", "µg/m³", "ppb", "ppb"],
    }
)


# Patch get_db_connect function
@patch("src.air_quality.data.get_db_connect.get_db_connect")
# Patch read_sql from pandas
@patch("src.air_quality.data.get_db_data.pd.read_sql")
def test_get_db_data_success(mock_get_db_connect, mock_read_sql):
    """Test ensures that function sucessfully connects to database and returns expected dataframe."""
    # Mock database connnection
    mock_engine = MagicMock()
    mock_get_db_connect.return_value = mock_engine
    # Mock pandas read_sql function to return mock_query_result
    mock_read_sql.return_value = mock_query_result
    # Call function with correct parameters
    return_df = get_db_data("user", "password", "localhost", "5432", "dbname")
    # Assert that the get_db_connect was called with correct parameters and SQL query was called properly
    mock_get_db_connect.assert_called_once_with(
        "user", "password", "localhost", "5432", "dbname"
    )
    mock_read_sql.assert_called_once_with(
        """
        SELECT
            datetime,
            parameter,
            value,
            unit
        FROM public.air_quality
        ORDER BY datetime DESC;
    """,
        mock_engine,
    )
    # Assert that returned dataframe is the same as mock query result
    pd.testing.assert_frame_equal(return_df, mock_query_result)


@patch("src.air_quality.data.get_db_connect.get_db_connect")
def test_get_db_data_connection_error(mock_get_db_connect):
    """Test ensures function properly handles database connection errors."""
    # Mock connection error
    mock_get_db_connect.side_effect = Exception("Failed to connect to database.")
    # Call function and assert it raises correct error
    with pytest.raises(OperationalError):
        get_db_data("user", "password", "localhost", "5432", "dbname")


@patch("src.air_quality.data.get_db_connect.get_db_connect")
@patch("src.air_quality.data.get_db_data.pd.read_sql")
def test_get_db_data_empty_result(mock_get_db_connect, mock_read_sql):
    """Test ensures that query returns empty dataframe when query returns empty."""
    # Mock database connection
    mock_engine = MagicMock()
    mock_get_db_connect.return_value = mock_engine
    # Mock read_sql function to return empty dataframe
    mock_read_sql.return_value = pd.DataFrame(
        columns=["datetime", "parameter", "value", "unit"]
    )
    # Call get_db_data function
    return_df = get_db_data("user", "password", "localhost", "5432", "dbname")
    # Assert returned df is empty
    assert return_df.empty
