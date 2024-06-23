import pandas as pd
import psycopg2

from air_quality.data.get_db_connect import get_db_connect


def get_db_data(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
    # Connects to postgresql database
    engine = get_db_connect(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

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
