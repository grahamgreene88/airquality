from unittest.mock import MagicMock, patch

import pandas as pd
import pytest
import streamlit as st
from pandas import Timestamp


@patch("src.air_quality.data.get_db_data.get_db_data")
@pytest.mark.skip
def test_dashboard_init(mock_get_db_data):
    """Ensures streamlit dashboard initializes correctly and data is properly loaded."""
    from src.air_quality.app import app

    # mock dataframe to be returned by get_db_data
    mock_data = {
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
    mock_df = pd.DataFrame(mock_data)
    mock_get_db_data.return_value = mock_df

    # run the streamlit app
    # from src.air_quality.app import app

    # Debugging prints
    print(app.pol_df.shape)
    print(app.pol_df.head())

    # assert dataframe is loaded correctly
    pd.testing.assert_frame_equal(app.pol_df, mock_df)
    # assert pollutants filter is correctly populated
    assert set(app.pol_list) == set(mock_df.parameter.unique())


@patch("src.air_quality.app.aq_index.calculate_AQHI")
@patch("src.air_quality.data.get_db_data.get_db_data")
@pytest.mark.skip
def test_aqhi_calc_integration(mock_get_db_data, mock_calculate_AQHI):
    """Tests that AQHI is calculated and displayed correctly on the dashboard."""
    # create mock dataframe
    mock_data = {
        "datetime": [
            Timestamp("2024-05-31 18:00:00+0000", tz="UTC"),
            Timestamp("2024-05-31 18:00:00+0000", tz="UTC"),
            Timestamp("2024-05-31 18:00:00+0000", tz="UTC"),
        ],
        "parameter": [
            "Particulate matter (PM2.5)",
            "Ozone (O3)",
            "Nitrogen dioxide (NO2)",
        ],
        "value": [4.0, 43.0, 2.0],
        "unit": ["µg/m³", "ppb", "ppb"],
    }
    mock_df = pd.DataFrame(mock_data)
    mock_get_db_data.return_value = mock_df
    mock_calculate_AQHI.return_value = 3

    # run streamlit app
    from src.air_quality.app import app

    # asssert calculate_AQHI is called with correct parameteres
    mock_calculate_AQHI.assert_called_once_with(2, 43, 4)

    # assert displayed AQHI value is correct
    assert app.AQHI == 3


@patch("src.air_quality.app.aq_index.calculate_AQHI")
@patch("src.air_quality.data.get_db_data.get_db_data")
def test_health_risk_color_determination(mock_get_db_data, mock_calculate_AQHI):
    # Create a mock dataframe
    mock_data = {
        "datetime": [
            Timestamp("2024-05-31 18:00:00+0000", tz="UTC"),
            Timestamp("2024-05-31 18:00:00+0000", tz="UTC"),
            Timestamp("2024-05-31 18:00:00+0000", tz="UTC"),
        ],
        "parameter": ["NO2", "O3", "PM2.5"],
        "value": [20, 30, 40],
        "unit": ["µg/m³", "ppb", "µg/m³"],
    }
    mock_df = pd.DataFrame(mock_data)
    mock_get_db_data.return_value = mock_df

    # Mock the calculate_AQHI return value
    mock_calculate_AQHI.return_value = 5

    # Run the app
    from src.air_quality.app import app

    # Check health risk and color determination logic
    assert app.health_risk == "Moderate"
    assert app.health_color == "#FFD700"
