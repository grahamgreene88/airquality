from unittest.mock import MagicMock, patch

import pytest
import pandas as pd
from pandas import Timestamp


# mock api variables
MOCK_API_KEY = "mock_api_key"
MOCK_DB_NAME = "mock_db_name"
MOCK_DB_USERNAME = "mock_user"
MOCK_DB_PASSWORD = "mock_password"
MOCK_DB_HOST = "mock_host"
MOCK_DB_PORT = "mock_port"

# mock data from api call and after cleaning data
mock_api_df = pd.DataFrame(
    {
        "locationId": [1275379, 1275379, 1275379],
        "location": ["Ottawa Downtown", "Ottawa Downtown", "Ottawa Downtown"],
        "parameter": ["pm25", "o3", "no2"],
        "value": [4.0, 0.043, 0.0],
        "unit": ["µg/m³", "ppm", "ppm"],
        "country": ["CA", "CA", "CA"],
        "city": [None, None, None],
        "isMobile": [False, False, False],
        "isAnalysis": [None, None, None],
        "entity": [
            "Governmental Organization",
            "Governmental Organization",
            "Governmental Organization",
        ],
        "sensorType": ["reference grade", "reference grade", "reference grade"],
        "date.utc": [
            "2024-05-31T18:00:00+00:00",
            "2024-05-31T18:00:00+00:00",
            "2024-05-31T18:00:00+00:00",
        ],
        "date.local": [
            "2024-05-31T14:00:00-04:00",
            "2024-05-31T14:00:00-04:00",
            "2024-05-31T14:00:00-04:00",
        ],
        "coordinates.latitude": [45.434333, 45.434333, 45.434333],
        "coordinates.longitude": [-75.67599, -75.67599, -75.67599],
    }
)

mock_cleaned_df = pd.DataFrame(
    {
        "datetime": [
            Timestamp("2024-05-31 14:00:00-0400", tz="UTC-04:00"),
            Timestamp("2024-05-31 14:00:00-0400", tz="UTC-04:00"),
            Timestamp("2024-05-31 14:00:00-0400", tz="UTC-04:00"),
        ],
        "parameter": [
            "Particulate matter (PM2.5)",
            "Ozone (O3)",
            "Nitrogen dioxide (NO2)",
        ],
        "value": [4.0, 43.0, 0.0],
        "unit": ["µg/m³", "ppb", "ppb"],
        "location": ["Ottawa Downtown", "Ottawa Downtown", "Ottawa Downtown"],
        "coordinates.latitude": [45.434333, 45.434333, 45.434333],
        "coordinates.longitude": [-75.67599, -75.67599, -75.67599],
    }
)


@patch("src.air_quality.data.get_api_data.get_api_data")
@patch("src.air_quality.data.clean_api_data.clean_api_data")
@patch("src.air_quality.data.get_db_connect.get_db_connect")
def test_main_workflow(mock_get_api_data, mock_clean_api_data, mock_get_db_connect):
    """General test to ensure main worflow runs properly."""
    # mock api data retrieval
    mock_get_api_data.return_value = mock_api_df
    # mock clean api data
    mock_clean_api_data.return_value = mock_cleaned_df
    # mock database connection
    mock_engine = MagicMock()
    mock_get_db_connect.return_value = mock_engine

    with patch("os.getenv") as mock_getenv:
        mock_getenv.side_effect = lambda key: {
            "API_KEY": MOCK_API_KEY,
            "DB_NAME": MOCK_DB_NAME,
            "DB_USERNAME": MOCK_DB_USERNAME,
            "DB_PASSWORD": MOCK_DB_PASSWORD,
            "DB_HOST": MOCK_DB_HOST,
            "DB_PORT": MOCK_DB_PORT,
        }[key]

        from src.air_quality.main import main

        # call main function
        main()

        # assert that functions work correctly
        mock_get_api_data.assert_called_once_with(MOCK_API_KEY)
        mock_clean_api_data.assert_called_once_with(mock_api_df)
        mock_get_db_connect.assert_called_once_with(
            MOCK_DB_NAME, MOCK_DB_USERNAME, MOCK_DB_PASSWORD, MOCK_DB_HOST, MOCK_DB_PORT
        )
        mock_engine.connect().assert_called()


if __name__ == "__main__":
    pytest.main()
