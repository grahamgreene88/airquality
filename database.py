import psycopg2

def create_table(db_connection, cursor):
    # Creating table in database
    create_table_query = """
        CREATE TABLE IF NOT EXISTS air_quality (
                date                TIMESTAMP,
                o3                  REAL,
                o3_unit             VARCHAR(50),
                pm25                REAL,
                pm25_unit           VARCHAR(50)
        );
    """
    # Run SQL query
    cursor.execute(create_table_query)
    # Save and commit changest to database
    db_connection.commit()
    
def insert_data(df, db_connection, cursor):
    insert_data_query = """
        INSERT INTO public.air_quality (
            date, o3, o3_unit, pm25, pm25_unit
        )
        VALUES (%s, %s, %s, %s, %s)
        
        ON CONFLICT (date) DO UPDATE SET
            o3 = EXCLUDED.o3,
            o3_unit = EXCLUDED.o3_unit
            pm25 = EXCLUDED.pm25
            pm25_unit = EXCLUDED.pm25_unit;
        """
            

        
    # query_string = insert_data_query % (
    #     f"TIMESTAMP '{df.loc[:, 'date'][0].isoformat()}'",
    #     *tuple(df.loc[:, 'o3']),
    #     f"'{df.loc[:, 'o3_unit'][0]}'",
    #     *tuple(df.loc[:, 'pm25']),
    #     f"'{df.loc[:, 'pm25_unit'][0]}'"
    # )
    # print(query_string)
    # cursor.execute(query_string)
    
    # cursor.execute(insert_data_query,
    #                (tuple(df.loc[:, 'date']),
    #                tuple(df.loc[:, 'o3']),
    #                tuple(df.loc[:, 'o3_unit']),
    #                tuple(df.loc[:, 'pm25']),
    #                tuple(df.loc[:, 'pm25_unit'])) 
    # )
    
    cursor.execute(insert_data_query,
                   (tuple(df['date']),
                   tuple(df['o3']),
                   tuple(df['o3_unit']),
                   tuple(df['pm25']),
                   tuple(df['pm25_unit']))
    )
    
    # Save and commit changest to database
    db_connection.commit()
    

      