from sqlalchemy import create_engine


def get_db_connect(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
    # Input validation for connection parameters
    if not DB_USERNAME or not DB_PASSWORD or not DB_HOST or not DB_PORT or not DB_NAME:
        raise ValueError("Invalid database connection parameters.")
    # Establishing database connection
    return create_engine(
        url="postgresql://{0}:{1}@{2}:{3}/{4}".format(
            DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
        )
    )
