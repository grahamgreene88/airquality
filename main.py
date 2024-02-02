import requests
import json
import pandas as pd
import logging
import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Importing custom scripts
from logger import config_logger
from api_pull import pull
from clean import clean_df
from database import create_table, insert_data
from database_alc import get_connection

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

# Clean pulled dataframe
final_df = clean_df(df)

# Connect to postgresql database
engine = get_connection(DB_USERNAME, DB_PASSWORD,
                        DB_HOST, DB_PORT, DB_NAME)

# Write data to table in postgresql database
final_df.to_sql('air_quality', engine, if_exists='replace', index=False)

