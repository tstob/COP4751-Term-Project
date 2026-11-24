import os
import mysql.connector
from mysql.connector import Error


# Connect to the existing job_tracker database
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=os.environ.get("MYSQL_PASSWORD", ""),
            database="job_tracker"
        )
        return connection

    except Error as e:
        print(f"Database connection error: {e}")
        return None
