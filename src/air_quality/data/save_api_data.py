import psycopg2


def create_table(db_conn):
    cursor = db_conn.cursor()
    # Creating table in database
    create_table_query = """
        CREATE TABLE IF NOT EXISTS air_quality (
                datetime            TIMESTAMP,
                parameter           TEXT,
                value               FLOAT8,
                unit                TEXT,
                location            TEXT,
                coordinates_latitude FLOAT8,
                coordinates_longitude FLOAT8,
                PRIMARY KEY (datetime, parameter)
        );
    """
    try:
        # Run SQL query
        cursor.execute(create_table_query)
        # Save and commit changes to database
        db_conn.commit()
        print("Table created successfully.")
    except psycopg2.Error as e:
        db_conn.rollback()
        print(f"Error occurred: {e}")
    finally:
        cursor.close()


def insert_data(df, db_conn):
    cursor = db_conn.cursor()
    insert_data_query = """
        INSERT INTO public.air_quality (
            datetime, parameter, value, unit, location, coordinates_latitude, coordinates_longitude
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (datetime, parameter) DO UPDATE SET
            value = EXCLUDED.value,
            unit = EXCLUDED.unit,
            location = EXCLUDED.location,
            coordinates_latitude = EXCLUDED.coordinates_latitude,
            coordinates_longitude = EXCLUDED.coordinates_longitude;
        """
    # Insert data from df row by row
    try:
        for index, row in df.iterrows():
            cursor.execute(
                insert_data_query,
                (
                    row["datetime"],
                    row["parameter"],
                    row["value"],
                    row["unit"],
                    row["location"],
                    row["coordinates_latitude"],
                    row["coordinates_longitude"],
                ),
            )
        db_conn.commit()
        print(f"Inserted {len(df)} rows of data.")
    # Rollback insertion if error occurs
    except Exception as e:
        db_conn.rollback()
        print(f"Error occured: {e}")
    finally:
        cursor.close()

    # cursor.execute(
    #     insert_data_query,
    #     (
    #         tuple(df["datetime"]),
    #         tuple(df["parameter"]),
    #         tuple(df["value"]),
    #         tuple(df["unit"]),
    #         tuple(df["location"]),
    #         tuple(df["coordinates_latitude"]),
    #         tuple(df["coordinates_longitude"]),
    #     ),
    # )

    # Save and commit changest to database
    # db_conn.commit()
