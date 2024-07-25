import psycopg2


def get_db_connect(DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
    # Input validation for connection parameters
    if not DB_USERNAME or not DB_PASSWORD or not DB_HOST or not DB_PORT or not DB_NAME:
        raise ValueError("Invalid database connection parameters.")
    # Configure db parameters
    db_param = {
        "dbname": DB_NAME,
        "user": DB_USERNAME,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": DB_PORT,
    }
    # Establishing database connection
    return psycopg2.connect(**db_param)
