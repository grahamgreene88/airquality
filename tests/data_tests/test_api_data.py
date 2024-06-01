import sys
import os

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from pandas import Timestamp

from src.air_quality.data.api_data import clean_api_data

# Ensure the root directory of the project is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Integration test
# def test_get_api_data():
    
@pytest.fixture
def sample_input_data():
    data = {
        'locationId': [1275379, 1275379, 1275379],
        'location': ['Ottawa Downtown', 'Ottawa Downtown', 'Ottawa Downtown'],
        'parameter': ['pm25', 'o3', 'no2'],
        'value': [4.0, 0.043, 0.0],
        'unit': ['µg/m³', 'ppm', 'ppm'],
        'country': ['CA', 'CA', 'CA'],
        'city': [None, None, None],
        'isMobile': [False, False, False],
        'isAnalysis': [None, None, None],
        'entity': ['Governmental Organization',
        'Governmental Organization',
        'Governmental Organization'],
        'sensorType': ['reference grade', 'reference grade', 'reference grade'],
        'date.utc': ['2024-05-31T18:00:00+00:00',
        '2024-05-31T18:00:00+00:00',
        '2024-05-31T18:00:00+00:00'],
        'date.local': ['2024-05-31T14:00:00-04:00',
        '2024-05-31T14:00:00-04:00',
        '2024-05-31T14:00:00-04:00'],
        'coordinates.latitude': [45.434333, 45.434333, 45.434333],
        'coordinates.longitude': [-75.67599, -75.67599, -75.67599]
        }
    return pd.DataFrame(data)

def test_clean_api_data(sample_input_data):
    """Tests entire functionality of clean_api_data.
    """
    expected_output = {
        'datetime': [Timestamp('2024-05-31 14:00:00-0400', tz='UTC-04:00'),
        Timestamp('2024-05-31 14:00:00-0400', tz='UTC-04:00'),
        Timestamp('2024-05-31 14:00:00-0400', tz='UTC-04:00')],
        'parameter': ['Particulate matter (PM2.5)',
        'Ozone (O3)',
        'Nitrogen dioxide (NO2)'],
        'value': [4.0, 43.0, 0.0],
        'unit': ['µg/m³', 'ppb', 'ppb'],
        'location': ['Ottawa Downtown', 'Ottawa Downtown', 'Ottawa Downtown'],
        'coordinates.latitude': [45.434333, 45.434333, 45.434333],
        'coordinates.longitude': [-75.67599, -75.67599, -75.67599]
        }
    expected_df = pd.DataFrame(expected_output)
    
    result_df = clean_api_data(sample_input_data)
    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))
