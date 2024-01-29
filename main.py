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
from database import create_table, insert_data

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
# Cleaning pulled dataframe
final_df = clean_df(df)

# Setup PostrgeSQL Database connection
db_connection = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT)
cursor = db_connection.cursor()

# Create Table in database
create_table(db_connection, cursor)

# Insert data into database
insert_data(final_df, db_connection, cursor)

# Close the cursor and database connection
cursor.close()
db_connection.close()