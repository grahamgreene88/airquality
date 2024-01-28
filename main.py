import requests
import json
import pandas as pd
import logging
import os
import psycopg2
from dotenv import load_dotenv

# Importing custom scripts
from logger import config_logger
from api_pull import pull
from clean import clean_df

# Loading hidden environment variables
load_dotenv()
API_KEY         =   os.getenv("API_KEY")
DB_NAME         =   os.getenv("DB_NAME")
DB_USERNAME     =   os.getenv("DB_USERNAME")
DB_PASSWORD     =   os.getenv("DB_PASSWORD")
DB_HOST         =   os.getenv("DB_HOST")
DB_PORT         =   os.getenv("DB_PORT")

# Configure logging
config_logger()

# Perform API pull
df = pull(API_KEY)
good_df = clean_df(df)
good_df

