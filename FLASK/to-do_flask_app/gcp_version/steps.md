CREATE DATABASE todo_db;
USE todo_db;

CREATE TABLE todos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'Pending'
);


- create data in mysql using above code

=========================================


2. connect data base
- in db.py
import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",   # Your MySQL host
        user="root",        # Your MySQL username
        password="your_password", # Your MySQL password
        database="todo_db"  # Database name
    )
    return connection

========================================
3. create requirements .txt for libraris
flask
mysql-connector-python

=======================================
