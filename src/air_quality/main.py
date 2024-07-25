import json
import logging
import os
import subprocess

from dotenv import load_dotenv
import pandas as pd
import psycopg2
import requests
from sqlalchemy import create_engine

# Importing custom scripts
from data.clean_api_data import clean_api_data
from data.get_api_data import get_api_data
from data.get_db_connect import get_db_connect
from data.save_api_data import create_table, insert_data

# Loading hidden environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def main():

    # Perform API pull
    df = get_api_data(API_KEY)

    # Clean pulled dataframe
    clean_df = clean_api_data(df)

    # Connect to postgresql database
    db_conn = get_db_connect(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    # Create air_quality table if it doesn't exist
    create_table(db_conn)

    # Save new air quality api data to postgress database
    insert_data(clean_df, db_conn)

    # Possible way to run streamlit app
    # construct app path to streamlit app
    app_path = os.path.join(os.path.dirname(__file__), "app", "app.py")
    # run streamlit app
    process = subprocess.Popen(["streamlit", "run", app_path])
    # put os.path.join() into input argument if app is not in same folder


if __name__ == "__main__":
    main()
