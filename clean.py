import pandas as pd

def clean_df(df):
    """cleans air quality dataframe into desired format.

    Args:
        df (dataframe): AQ dataframe pulled from API.
    """
    small_df = df.loc[:, ['date.local', 'parameter', 'value', 'unit']]
    pivot_df = small_df.pivot(index='date.local', columns='parameter', values='value')
    pivot_df.reset_index()
    pivot_df = pivot_df.rename_axis(None, axis=1)
    # Inserting column for pollutant units, location, latitude, longitude
    pivot_df.insert(1, 'no2_unit', 'ppm')
    pivot_df.insert(3, 'o3_unit', 'ppm')
    pivot_df.insert(5, 'pm25_unit', 'µg/m³')
    pivot_df['location'] = 'Downtown Ottawa'
    pivot_df[['coordinates.latitude', 'coordinates.longitude']] = (45.434333, -75.67599)
    final_df = pivot_df.reset_index()
    # Changing lastupdated column name to date
    final_df.rename(columns={'date.local': 'datetime'}, inplace=True)
    # Changing date column to datetime data type
    final_df['datetime'] = pd.to_datetime(final_df['datetime'])
    final_df.sort_values('datetime', ascending=False, inplace=True)
    return final_df
    
    
    