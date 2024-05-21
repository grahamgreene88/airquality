from sqlalchemy import create_engine
import psycopg2

def get_connection(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
        )
    )
    