import mysql.connector
import os 
from secret_key import *

def get_db_connection():
    connection = mysql.connector.connect(
        host     =os.getenv("DB_HOST"),   # Your MySQL host
        user     =os.getenv("DB_USER"),   # Your MySQL username
        password =os.getenv("DB_PASSWORD"),   # Your MySQL password
        database =os.getenv("DB_NAME")       # Database name
    )
    return connection

# in secrect.py
# db_username= "root"
# db_password = "Azsxdcf123@"
# db_name = "todos"