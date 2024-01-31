import pandas as pd
import os
from dotenv import load_dotenv
from database_alc import get_connection

def database_pull(DB_USERNAME, DB_PASSWORD,
                        DB_HOST, DB_PORT, DB_NAME):
    # Connect to postgresql database
    engine = get_connection(DB_USERNAME, DB_PASSWORD,
                        DB_HOST, DB_PORT, DB_NAME)
    
    # Query for air quality data from posgtreSQL
    get_new_data_query = """
        SELECT
            date,
            o3,
            o3_unit,
            pm25,
            pm25_unit
        FROM public.air_quality
        ORDER BY date DESC
        Limit 1;
    """
    
    # Read database data into dataframe
    app_df = pd.read_sql(get_new_data_query, engine)
    return app_df