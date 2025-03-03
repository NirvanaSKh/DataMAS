from config.db_config import get_db_connection
import pandas as pd

def query_database(sql_query):
    try:
        conn = get_db_connection()
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return df
    except Exception as e:
        return None
