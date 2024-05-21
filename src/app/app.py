import os

import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import plotly.express as px

from src.data.database.db_pull import database_pull
from src.app.aq_index import calculate_AQHI

# Loading hidden environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
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
 #   initial_sidebar_state="expanded")
)

# Add dashboard title
st.title("Air Quality Monitoring - Downtown Ottawa")

# Add pollutant filter
pol_list = list(pol_df.parameter.unique())
selected_pol = st.selectbox('Select a pollutant', pol_list, index=1)
df_selected_pol = pol_df[pol_df.parameter == selected_pol]
selected_unit = str(df_selected_pol.unit.unique())

# # Setup time filter
# timeframe_list = ['Past week', 'Past 3 days', 'Past 24 hours']
# selected_timeframe = st.selectbox("Select a timeframe", timeframe_list, index=1)
# if selected_timeframe == 'Past week':
#     df_selected_pol = df_selected_pol
# if selected_timeframe == 'Past 3 days':
#     df_selected_pol = 
    

# air quality concentration chart over time
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
col = st.columns((12, 3), gap='medium')

# Plot air quality chart in first column
with col[0]:
    st.markdown('### Past Week')
    st.plotly_chart(fig_line, use_container_width=True, width = 1000, height=500)

# Add current air quality index for selected pollutant
current_no2 = pol_df[pol_df.parameter == 'Nitrogen dioxide (NO2)'].iloc[0]['value']
current_o3 = pol_df[pol_df.parameter == 'Ozone (O3)'].iloc[0]['value']
current_pm25 = pol_df[pol_df.parameter == 'Particulate matter (PM2.5)'].iloc[0]['value']

# Calculate current air quality health index
AQHI = calculate_AQHI(current_no2, current_o3, current_pm25)
# Determine health risk and corresponding color
if AQHI <= 3:
    health_risk = 'Low'
    if AQHI == 1:
        health_color = '#00BFFF'
    if AQHI == 2:
        health_color = '#0000CD'
    else:
        health_color = '#00008B'
elif AQHI > 3 and AQHI <= 6:
    health_risk = 'Moderate'
    if AQHI == 4:
        health_color = '#FFFF00'
    if AQHI == 5:
        health_color = '#FFD700'
    else:
        health_color = '#FF8C00' 
elif AQHI > 6 and AQHI <= 10:
    health_risk = 'High'
    if AQHI == 7:
        health_color = '#FF6347'
    if AQHI == 8:
        health_color = '#FF0000'
    if AQHI == 9:
        health_color = '#B22222'
    else:
        health_color = '#8B0000'
elif AQHI > 10:
    health_risk = 'Very High'
    health_color = '#000000'

# Populate second column with metrics
with col[1]:
    # second column header
    st.header("Current Measurements")
    # selected pollutant - current concentration
    if selected_pol == "Particulate matter (PM2.5)":
        display_text = "PM2.5"
        display_pol = current_pm25
        display_unit = "µg/m³"
    if selected_pol == "Ozone (O3)":
        display_text = "O3"
        display_pol = current_o3
        display_unit = "ppb"
    if selected_pol == "Nitrogen dioxide (NO2)":
        display_text = "NO2"
        display_pol = current_no2
        display_unit = "ppb"
    st.metric(label=f"Current {display_text} concentration:", value=f"{display_pol} {display_unit}")
    
    # current AQHI
    st.metric(label="Air Quality Health Index (AQHI)", value=AQHI)
    # current health risk
    st.metric(label="Health Risk", value=health_risk)
    style_metric_cards(border_left_color=health_color)
    
# Creating dataframe with health messages
health_messages_dict = {
    'Health Risk': ['Low', 'Moderate', 'High', 'Very High'],
    'AQHI': ['1-3', '4-6', '7-10', 'Above 10'],
    'At Risk Population': ['Enjoy your usual outdoor activities.', 
                           'Consider reducing or rescheduling strenuous activities outdoors if you are experiencing symptoms.',
                           'Reduce or reschedule strenuous activities outdoors. Children and the elderly should also take it easy.', 
                           'Avoid strenuous activities outdoors. Children and the elderly should also avoid outdoor physical exertion.'],
    'General Population': ['Ideal air quality for outdoor activities.', 
                           'No need to modify your usual outdoor activities unless you experience symptoms such as coughing and throat irritation.', 
                           'Consider reducing or rescheduling strenuous activities outdoors if you experience symptoms such as coughing and throat irritation.',
                           'Reduce or reschedule strenuous activities outdoors, especially if you experience symptoms such as coughing and throat irritation.']
}
health_messages_df = pd.DataFrame(health_messages_dict)
# health_messages_df.set_index('Health Risk', inplace=True)
# health_messages_df['At Risk Population'] = health_messages_df['At Risk Population'].str.wrap(20)
# health_messages_df['General Population'] = health_messages_df['General Population'].str.wrap(20)
# health_messages_df.set_index('Health Risk', inplace=True)
health_messages_df.style.hide(axis=0)
   
# with col[0]:
#     # st.dataframe(health_messages_df[health_messages_df['Health Risk'] == health_risk], use_container_width=True, hide_index=True)
#     st.dataframe(health_messages_df, use_container_width=True, hide_index=True)

with col[0]:
    st.table(health_messages_df[health_messages_df['Health Risk'] == health_risk])
    #st.table(health_messages_df)
             #, use_container_width=True, hide_index=True)
