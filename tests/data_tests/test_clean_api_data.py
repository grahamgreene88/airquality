import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from pandas import Timestamp

from src.air_quality.data.api_data import clean_api_data
    
@pytest.fixture
def sample_input_data():
    # Fixture setup
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
    df = pd.DataFrame(data)
    # Fixture output
    yield df
    # Fixture teardown
    df.drop(df.index, inplace=True)
    del df


def test_clean_api_data(sample_input_data):
    """Tests entire functionality of clean_api_data function."""
    # Expected output from function achieved by manually wrangling
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
    # Dataframe achieved from using function
    result_df = clean_api_data(sample_input_data)
    # Assert statement compares df from function and df from manual wrangling
    assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))


def test_empty_dataframe():
    """Tests cleaning function with an empty dataframe as input."""
    # Empty dataframe with all input columns
    empty_df = pd.DataFrame(columns=['locationId', 'location', 'parameter', 'value', 'unit', 'country',
       'city', 'isMobile', 'isAnalysis', 'entity', 'sensorType', 'date.utc',
       'date.local', 'coordinates.latitude', 'coordinates.longitude'])
    # Testing function on empty df
    result_empty_df = clean_api_data(empty_df)
    # Expected dataframe with only output columns
    expected_empty_df = pd.DataFrame(columns=['datetime', 'parameter', 'value', 'unit', 'location',
       'coordinates.latitude', 'coordinates.longitude'])
    expected_empty_df['datetime'] = pd.to_datetime(expected_empty_df['datetime'])
    # Assert statement compares empty df from function and manually-created empty df
    assert_frame_equal(result_empty_df, expected_empty_df)
    
    
def test_missing_columns(sample_input_data):
    """Tests that KeyError is raised if dataframe is missing one of the output
    columns. No error is raised if one of the dropped columns is missing."""
    df_missing = sample_input_data.drop(columns=['value'])
    with pytest.raises(KeyError):
        clean_api_data(df_missing)
        

def test_no_subset_matches(sample_input_data):
    """Tests function when no rows match the subset condition."""
    # Input dataframe without subsetted rows
    no_subset_df = sample_input_data[sample_input_data['parameter'] == 'pm25']
    result_no_subset_df = clean_api_data(no_subset_df)
    # Expected output dataframe if functionality is preserved
    expected_df = no_subset_df.copy()
    expected_df = expected_df.loc[:, ['date.local', 'parameter', 'value', 'unit', 'location', 'coordinates.latitude', 'coordinates.longitude']]
    expected_df.sort_values('date.local', ascending=False, inplace=True)
    expected_df['parameter'] = expected_df['parameter'].replace({'pm25': 'Particulate matter (PM2.5)'})
    expected_df = expected_df.rename(columns={'date.local': 'datetime'})
    expected_df['datetime'] = pd.to_datetime(expected_df['datetime'])
    # Assert statement that compares df from function with no rows to subset with manually wrangled df
    assert_frame_equal(result_no_subset_df, expected_df)
    
    