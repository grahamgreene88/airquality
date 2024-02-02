import requests
import json
import pandas as pd
import logging
from requests import HTTPError, Timeout, RequestException
from datetime import datetime, timedelta
from urllib.parse import quote

def pull(API_KEY):
    """This function pulls data from the OpenAQ API to obtain the pollutant, value, update time, and unit
    for the last seven days.
    
    
    Args:
        API_KEY from .env file.

    Returns:
        Dataframe with 4 columns and 2 rows. One row for each pollutant.
        
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
        logger.error(f"HTTP error occurred: {http_err}")
        
    except Timeout:
        logger.error("Request timed out after 15 seconds.")
        
    except RequestException as request_err:
        logger.error("Request error occurred: {request_err}")

    aq_data = json.loads(response.text)
    aq_df = pd.json_normalize(aq_data['results'])
    return aq_df

