import requests
import json
import pandas as pd
from requests import HTTPError, Timeout, RequestException
from datetime import datetime, timedelta
from urllib.parse import quote

def get_api_data(API_KEY):
    """This function pulls data from the OpenAQ API to obtain air quality data for Downtown Ottawa
    for the last seven days.
    
    
    Args:
        API_KEY from .env file.

    Returns:
        Dataframe with 15 columns and however many records (as rows) occured in the past 7 days.
        
    Raises:
        HTTPError, Timeout and RequestException
    """

    # Get datetimes for present and one week ago
    current_datetime = datetime.utcnow()
    week_ago_datetime = current_datetime - timedelta(days=7)
    # Format datetimes to ISO 8601
    date_from = week_ago_datetime.isoformat()
    date_to = current_datetime.isoformat()
    
    # Insert date_from and date_to into API url
    url = f"https://api.openaq.org/v2/measurements?date_from={quote(date_from)}&date_to={quote(date_to)}&limit=1000&page=1&offset=0&sort=desc&has_geo=true&parameter=o3&parameter=pm25&parameter=no2&location_id=1275379&order_by=datetime"

    headers = {
        "X-API-Key": API_KEY,
        "accept": "application/json"}

    session = requests.Session()
    session.headers.update(headers)

    # try-except blocks for robust error handling and logging
    try:
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
    
    except HTTPError as http_err:
        raise http_err
        # logger.error(f"HTTP error occurred: {http_err}")
        
    except Timeout as timeout_err:
        raise timeout_err
        # logger.error("Request timed out after 15 seconds.")
        
    except RequestException as request_err:
        raise request_err
        # logger.error("Request error occurred: {request_err}")

    aq_data = json.loads(response.text)
    aq_df = pd.json_normalize(aq_data['results'])
    return aq_df

def clean_api_data(df):
    """cleans air quality dataframe into desired format.

    Args:
        df (dataframe): AQ dataframe pulled from API.
    """
    # Select desired columns
    small_df = df.loc[:, ['date.local', 'parameter', 'value', 'unit', 'location', 'coordinates.latitude', 'coordinates.longitude']]
    # Sort by date descending
    small_df.sort_values('date.local', ascending=False, inplace=True)
    # Convert ppm units to ppb
    subset = (small_df['parameter'] == 'o3') | (small_df['parameter'] == 'no2')
    small_df.loc[subset, 'value'] *= 1000
    small_df.loc[subset, 'unit'] = 'ppb'
    # Replace pollutant names with full written names
    small_df['parameter'] = small_df['parameter'].replace({'pm25': 'Particulate matter (PM2.5)', 'no2': 'Nitrogen dioxide (NO2)', 'o3': 'Ozone (O3)'})
    # Changing column name to datetime
    small_df = small_df.rename(columns={'date.local': 'datetime'})
    # Changing datetime column to datetime data type
    small_df['datetime'] = pd.to_datetime(small_df['datetime'])
    return small_df