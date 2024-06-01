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
from data.api_data import get_api_data
from data.api_data import clean_api_data
# from src.data.database.database import create_table, insert_data
from data.data_storage import get_db_connection

import subprocess

# Loading hidden environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def main():
    # Configure logging
    config_logger()

    # Perform API pull
    df = get_api_data(API_KEY)

    # Clean pulled dataframe
    final_df = clean_api_data(df)

    # Connect to postgresql database
    engine = get_db_connection(DB_USERNAME, DB_PASSWORD,
                            DB_HOST, DB_PORT, DB_NAME)

    # Write data to table in postgresql database
    final_df.to_sql('air_quality', engine, if_exists='replace', index=False)
    
    # Possible way to run streamlit app
    # construct app path to streamlit app
    app_path = os.path.join(os.path.dirname(__file__), 'app', 'app.py')
    # run streamlit app
    process = subprocess.Popen(["streamlit", "run", app_path])
    # put os.path.join() into input argument if app is not in same folder

if __name__ == "__main__":
    main()