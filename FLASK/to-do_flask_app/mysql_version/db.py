
import mysql.connector

from secret_key import *

def get_db_connection():
    connection = mysql.connector.connect(
        host     ="localhost",   # Your MySQL host
        user     =db_username,   # Your MySQL username
        password =db_password,   # Your MySQL password
        database =db_name        # Database name
    )
    return connection



# in secrect.py
# db_username= "root"
# db_password = "Azsxdcf123@"
# db_name = "todos"