import pandas as pd

def clean_df(df):
    """cleans air quality dataframe into desired format.

    Args:
        df (dataframe): AQ dataframe pulled from API.
    """
    pivot_df = df.pivot(index='lastUpdated', columns='parameter', values='value')
    pivot_df.reset_index()
    pivot_df = pivot_df.rename_axis(None, axis=1)
    # Inserting column for pollutant units
    pivot_df.insert(1, 'o3_unit', 'ppm')
    pivot_df['pm25_unit'] = ['µg/m³']
    final_df = pivot_df.reset_index()
    # Changing lastupdated column name to date
    final_df.rename(columns={'lastUpdated': 'date'}, inplace=True)
    # Changing date column to datetime data type
    final_df['date'] = pd.to_datetime(final_df['date'])
    return final_df
    
    
    