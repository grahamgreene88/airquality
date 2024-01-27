import requests
import json
import pandas as pd
import logging
from requests import HTTPError, Timeout, RequestException

def api_pull():
    """This function pulls data from the OpenAQ API to obtain the pollutant, value, update time, and unit.
    
Args:
    None.

Returns:
    Dataframe with 4 columns and 2 rows. One row for each pollutant.
    
Raises:
    HTTPError, Timeout and RequestException
    """

    url = "https://api.openaq.org/v2/latest/498?limit=100&page=1&offset=0&sort=asc"

    headers = {
        "X-API-Key": "5eb79066433eb416b9a688101dfba9b40f44ffbbd58f913d2f8aafd4867395e5",
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
    aq_df = pd.json_normalize(aq_data['results'], record_path=['measurements'])
    return aq_df

