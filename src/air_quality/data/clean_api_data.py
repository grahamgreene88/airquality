import pandas as pd


def clean_api_data(df):
    """cleans air quality dataframe into desired format.

    Args:
        df (dataframe): AQ dataframe pulled from API.
    """
    # Select desired columns
    small_df = df.loc[
        :,
        [
            "date.local",
            "parameter",
            "value",
            "unit",
            "location",
            "coordinates.latitude",
            "coordinates.longitude",
        ],
    ]
    # Sort by date descending
    small_df.sort_values("date.local", ascending=False, inplace=True)
    # Convert ppm units to ppb
    subset = (small_df["parameter"] == "o3") | (small_df["parameter"] == "no2")
    small_df.loc[subset, "value"] *= 1000
    small_df.loc[subset, "unit"] = "ppb"
    # Replace pollutant names with full written names
    small_df["parameter"] = small_df["parameter"].replace(
        {
            "pm25": "Particulate matter (PM2.5)",
            "no2": "Nitrogen dioxide (NO2)",
            "o3": "Ozone (O3)",
        }
    )
    # Changing column name to datetime
    small_df = small_df.rename(columns={"date.local": "datetime"})
    # Changing datetime column to datetime data type
    small_df["datetime"] = pd.to_datetime(small_df["datetime"])
    return small_df
