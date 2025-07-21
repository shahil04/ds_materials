import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",   # Your MySQL host
        user="root",        # Your MySQL username
        password="Azsxdcf123@", # Your MySQL password
        database="todo_db"  # Database name
    )
    return connection
