from sqlalchemy import create_engine
import psycopg2

import pandas as pd
import os
from dotenv import load_dotenv


def get_db_connection(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
    # Input validation for connection parameters
    if not DB_USERNAME or not DB_PASSWORD or not DB_HOST or not DB_PORT or not DB_NAME:
        raise ValueError("Invalid database connection parameters.")
    # Establishing database connection
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
        )
    )


def get_db_data(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
    # Connect to postgresql database
    engine = get_db_connection(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    # Query for air quality data from posgtreSQL
    get_new_data_query = """
        SELECT
            datetime,
            parameter,
            value,
            unit
        FROM public.air_quality
        ORDER BY datetime DESC;
    """

    # Read database data into dataframe
    app_df = pd.read_sql(get_new_data_query, engine)
    return app_df
