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

pol_df = database_pull(DB_USERNAME, DB_PASSWORD,
                        DB_HOST, DB_PORT, DB_NAME)

# Set up streamlit dashboard
st.set_page_config(
    page_title = "Air Quality Dashboard",
    page_icon =  '😶‍🌫️',
    layout="wide",
    initial_sidebar_state="expanded")

# Add dashboard title
st.title("Air Quality Monitoring - Downtown Ottawa")

with st.sidebar:
    st.title("Air Quality Dashboard 😶‍🌫️")
    
    pol_list = list(pol_df.parameter.unique())
    
    selected_pol = st.selectbox('Select a pollutant', pol_list, index=1)
    df_selected_pol = pol_df[pol_df.parameter == selected_pol]
    selected_unit = str(df_selected_pol.unit.unique())

y_axis_name = 'Concentration' + ' ' + '(' + selected_unit + ')'

fig_line = px.line(df_selected_pol,
        x='datetime',
        y='value',
        labels={'value': y_axis_name,
                'datetime': 'Date'},
        width=1000,
        height=500)
# fig_line.update_traces(patch=)

# Dashboard layout
col = st.columns((5, 3), gap='medium')

with col[0]:
    st.markdown('### Past Week')
    st.plotly_chart(fig_line, use_container_width=True, width = 1000, height=500)

# Add current air quality index for selected pollutant
with col[1]:
    st.metric(label='Air Quality Index', )

if selected_pol = "Ozone (O3)":
    if df_selected_pol.iloc[1, 2] > 5:
        aqi = 'Low'
elif selected_pol = "Nitrogen dioxide (NO2)":
    
else:
    
    



