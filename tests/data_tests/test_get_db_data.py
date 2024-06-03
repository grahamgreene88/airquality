from unittest.mock import patch, MagicMock

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from pandas import Timestamp

from src.air_quality.data.data_storage import get_db_data, get_db_connection

# Mock expected data to be returned from SQL query
mock_query = pd.DataFrame({
    'datetime': [Timestamp('2024-05-31 18:00:00+0000', tz='UTC'),
    Timestamp('2024-05-31 18:00:00+0000', tz='UTC'),
    Timestamp('2024-05-31 18:00:00+0000', tz='UTC'),
    Timestamp('2024-05-31 17:00:00+0000', tz='UTC'),
    Timestamp('2024-05-31 17:00:00+0000', tz='UTC'),
    Timestamp('2024-05-31 17:00:00+0000', tz='UTC')],
    'parameter': ['Particulate matter (PM2.5)',
    'Ozone (O3)',
    'Nitrogen dioxide (NO2)',
    'Particulate matter (PM2.5)',
    'Nitrogen dioxide (NO2)',
    'Ozone (O3)'],
    'value': [4.0, 43.0, 0.0, 4.0, 0.0, 43.0],
    'unit': ['µg/m³', 'ppb', 'ppb', 'µg/m³', 'ppb', 'ppb']}
)

