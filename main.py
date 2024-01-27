import requests
import json
import pandas as pd
import logging
import os

from logger import config_logger
from api_pull import api_pull


# Configure logging
config_logger()

# Perform API pull
api_pull()
