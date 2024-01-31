import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
import plotly.express as px

from db_pull import database_pull

# Loading hidden environment variables
load_dotenv()
API_KEY         =   os.getenv("API_KEY")
DB_NAME         =   os.getenv("DB_NAME")
DB_USERNAME     =   os.getenv("DB_USERNAME")
DB_PASSWORD     =   os.getenv("DB_PASSWORD")
DB_HOST         =   os.getenv("DB_HOST")
DB_PORT         =   os.getenv("DB_PORT")

new_data_df = database_pull(DB_USERNAME, DB_PASSWORD,
                        DB_HOST, DB_PORT, DB_NAME)
new_data_df

# Set up streamlit dashboard
st.set_page_config(
    page_title = "Air Quality Dashboard",
    layout="wide"
)

# Add main title
st.title("Air Quality Monitoring - Ottawa, ON")




