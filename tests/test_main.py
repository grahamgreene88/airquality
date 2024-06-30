from unittest.mock import MagicMock, patch

import pytest

from src.air_quality.main import main

# mock api variables
API_KEY = "mock_api_key"
DB_NAME = "mock_db_name"
DB_USERNAME = "mock_user"
DB_PASSWORD = "mock_password"
DB_HOST = "mock_host"
DB_PORT = "mock_port"

# mock data from api call and after cleaning data
mock_api_data = {
    "locationId": [1275379, 1275379, 1275379],
    "location": ["Ottawa Downtown", "Ottawa Downtown", "Ottawa Downtown"],
    "parameter": ["pm25", "pm25", "pm25"],
    "value": [4.0, 4.0, 4.0],
    "unit": ["µg/m³", "µg/m³", "µg/m³"],
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
        "2024-05-31T17:00:00+00:00",
        "2024-05-31T16:00:00+00:00",
    ],
    "date.local": [
        "2024-05-31T14:00:00-04:00",
        "2024-05-31T13:00:00-04:00",
        "2024-05-31T12:00:00-04:00",
    ],
    "coordinates.latitude": [45.434333, 45.434333, 45.434333],
    "coordinates.longitude": [-75.67599, -75.67599, -75.67599],
}
df = pd.DataFrame(data)
