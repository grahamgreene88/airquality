from unittest.mock import patch, MagicMock

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from pandas import Timestamp

from src.air_quality.data.data_storage import get_db_data, get_db_connection

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


# Patch get_db_connection function
@patch("src.air_quality.data.data_storage.get_db_connection")
# Patch read_sql from pandas
@patch("src.air_quality.data.data_storage.pd.read_sql")
def test_get_db_data_success(mock_get_db_connection, mock_read_sql):
    """Test ensures that function sucessfully connects to database and returns expected dataframe."""
    # Mock database connnection
    mock_engine = MagicMock()
    mock_get_db_connection.return_value = mock_engine
    # Mock pandas read_sql function to return mock_query_result
    mock_read_sql.return_value = mock_query_result
    # Call function with correct parameters
    df = get_db_data("user", "password", "localhost", "5432", "dbname")
    # Asser that the inner function get_db_connection was called with correct parameters
    # is this test not redundant with test for get_db_connection?
