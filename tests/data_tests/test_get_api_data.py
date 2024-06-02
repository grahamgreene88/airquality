import json
from unittest.mock import patch
from datetime import datetime, timedelta

import pytest
import requests
from requests import HTTPError, Timeout, RequestException
import pandas as pd
from pandas.testing import assert_frame_equal

from src.air_quality.data.api_data import get_api_data

# Mock API response from a successul API call
mock_api_response = {
    'meta': {
        'name': 'openaq-api',
        'license': '',
        'website': '/',
        'page': 1,
        'limit': 1000,
        'found': 57
  },
 'results': [
     {
         'locationId': 1275379,
        'location': 'Ottawa Downtown',
        'parameter': 'pm25',
        'value': 4.0,
        'date': {'utc': '2024-05-31T18:00:00+00:00','local': '2024-05-31T14:00:00-04:00'},
        'unit': 'µg/m³',
        'coordinates': {'latitude': 45.434333, 'longitude': -75.67599},
        'country': 'CA',
        'city': None,
        'isMobile': False,
        'isAnalysis': None,
        'entity': 'Governmental Organization',
        'sensorType': 'reference grade'
        },
     {
         'locationId': 1275379,
        'location': 'Ottawa Downtown',
        'parameter': 'pm25',
        'value': 4.0,
        'date': {'utc': '2024-05-31T17:00:00+00:00','local': '2024-05-31T13:00:00-04:00'},
        'unit': 'µg/m³',
        'coordinates': {'latitude': 45.434333, 'longitude': -75.67599},
        'country': 'CA',
        'city': None,
        'isMobile': False,
        'isAnalysis': None,
        'entity': 'Governmental Organization',
        'sensorType': 'reference grade'
        },
     {
         'locationId': 1275379,
        'location': 'Ottawa Downtown',
        'parameter': 'pm25',
        'value': 4.0,
        'date': {'utc': '2024-05-31T16:00:00+00:00','local': '2024-05-31T12:00:00-04:00'},
        'unit': 'µg/m³',
        'coordinates': {'latitude': 45.434333, 'longitude': -75.67599},
        'country': 'CA',
        'city': None,
        'isMobile': False,
        'isAnalysis': None,
        'entity': 'Governmental Organization',
        'sensorType': 'reference grade'
        }
     ]
 }

# Fixture for expected dataframe from API call
@pytest.fixture
def expected_api_df():
    data = {
        'locationId': [1275379, 1275379, 1275379],
        'location': ['Ottawa Downtown', 'Ottawa Downtown', 'Ottawa Downtown'],
        'parameter': ['pm25', 'pm25', 'pm25'],
        'value': [4.0, 4.0, 4.0],
        'unit': ['µg/m³', 'µg/m³', 'µg/m³'],
        'country': ['CA', 'CA', 'CA'],
        'city': [None, None, None],
        'isMobile': [False, False, False],
        'isAnalysis': [None, None, None],
        'entity': ['Governmental Organization', 'Governmental Organization', 'Governmental Organization'],
        'sensorType': ['reference grade', 'reference grade', 'reference grade'],
        'date.utc': ['2024-05-31T18:00:00+00:00', '2024-05-31T17:00:00+00:00', '2024-05-31T16:00:00+00:00'],
        'date.local': ['2024-05-31T14:00:00-04:00', '2024-05-31T13:00:00-04:00', '2024-05-31T12:00:00-04:00'],
        'coordinates.latitude': [45.434333, 45.434333, 45.434333],
        'coordinates.longitude': [-75.67599, -75.67599, -75.67599]
        }
    df = pd.DataFrame(data)
    # Fixture output
    yield df
    # Fixture teardown
    df.drop(df.index, inplace=True)
    del df
    
@patch('src.air_quality.data.api_data.requests.get')
def test_get_api_data_success(mock_get, expected_api_df):
    """Tests a successful API call and the resulting dataframe that is returned."""
    # Set status code of mock response to successful HTTP request
    mock_get.return_value.status_code = 200
    # Set content of mock JSON response to mock api response
    mock_get.return_value.json.return_value = mock_api_response
    df = get_api_data('fake_key')
    # Comparing df from mock response with expected df
    assert_frame_equal(df, expected_api_df)

    
    