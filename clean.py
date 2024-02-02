import pandas as pd

def clean_df(df):
    """cleans air quality dataframe into desired format.

    Args:
        df (dataframe): AQ dataframe pulled from API.
    """
    # Select desired columns
    small_df = df.loc[:, ['date.local', 'parameter', 'value', 'unit', 'location', 'coordinates.latitude', 'coordinates.longitude']]
    # Sort by date descending
    small_df.sort_values('date.local', ascending=False, inplace=True)
    # Replace pollutant names with full written names
    small_df['parameter'] = small_df['parameter'].replace({'pm25': 'Particulate matter (pm25)', 'no2': 'Nitrogen dioxide (NO2)', 'o3': 'Ozone (O3)'})
    # Changing column name to datetime
    small_df = small_df.rename(columns={'date.local': 'datetime'})
    # Changing datetime column to datetime data type
    small_df['datetime'] = pd.to_datetime(small_df['datetime'])
    return small_df
    
    
    
    
    # small_df = df.loc[:, ['date.local', 'parameter', 'value', 'unit']]
    # pivot_df = small_df.pivot(index='date.local', columns='parameter', values='value')
    # pivot_df.reset_index()
    # pivot_df = pivot_df.rename_axis(None, axis=1)
    # # Inserting column for pollutant units, location, latitude, longitude
    # pivot_df.insert(1, 'no2_unit', 'ppm')
    # pivot_df.insert(3, 'o3_unit', 'ppm')
    # pivot_df.insert(5, 'pm25_unit', 'µg/m³')
    # pivot_df['location'] = 'Downtown Ottawa'
    # pivot_df[['coordinates.latitude', 'coordinates.longitude']] = (45.434333, -75.67599)
    # final_df = pivot_df.reset_index()
    # # Changing lastupdated column name to date
    # final_df.rename(columns={'date.local': 'datetime'}, inplace=True)
    # # Changing date column to datetime data type
    # final_df['datetime'] = pd.to_datetime(final_df['datetime'])
    # final_df.sort_values('datetime', ascending=False, inplace=True)