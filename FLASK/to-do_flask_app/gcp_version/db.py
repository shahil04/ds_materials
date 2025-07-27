import mysql.connector

GCP_PUBLIC_IP = "34.67.229.167"
DB_USERNAME = "root2"
DB_PASSWORD = "Azsxdcf123@"
DB_NAME = "todo_db"

def get_db_connection():
    connection = mysql.connector.connect(
        host=GCP_PUBLIC_IP,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return connection

db = get_db_connection()  # Call the function with ()