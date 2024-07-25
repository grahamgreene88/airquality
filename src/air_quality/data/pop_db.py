import requests
import json
import pandas as pd
from requests import HTTPError, Timeout, RequestException
from datetime import datetime, timedelta


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

    # url = "https://api.openaq.org/v2/measurements?date_from=2023-07-17T00%3A00%3A00Z&date_to=2024-01-01T00%3A00%3A00Z&limit=20000&page=1&sort=desc&parameter=pm25&parameter=o3&parameter=no2&radius=1000&location_id=1275379&order_by=datetime"
    # url = "https://api.openaq.org/v2/measurements?date_from=2024-01-01T01%3A00%3A00Z&date_to=2024-05-01T00%3A00%3A00Z&limit=20000&page=1&sort=desc&parameter=pm25&parameter=o3&parameter=no2&radius=1000&location_id=1275379&order_by=datetime"
    # url = "https://api.openaq.org/v2/measurements?date_from=2024-05-01T01%3A00%3A00Z&date_to=2024-07-11T00%3A00%3A00Z&limit=20000&page=1&sort=desc&parameter=pm25&parameter=o3&parameter=no2&radius=1000&location_id=1275379&order_by=datetime"
    url = "https://api.openaq.org/v2/latest/1275379?limit=100&page=1&offset=0&sort=asc"

    headers = {"X-API-Key": API_KEY, "accept": "application/json"}

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
    results = aq_data["results"]

    aq_df = pd.json_normalize(
        results,
        record_path=["measurements"],
        meta=[
            "location",
            "city",
            "country",
            ["coordinates", "latitude"],
            ["coordinates", "longitude"],
        ],
    )
    # aq_df = pd.json_normalize(aq_data["results"])

    return aq_df
