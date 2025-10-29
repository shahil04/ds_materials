import os, pymysql
from dotenv import load_dotenv
load_dotenv()
DB_HOST=os.getenv("DB_HOST");DB_PORT=int(os.getenv("DB_PORT",3306))
DB_USER=os.getenv("DB_USER");DB_PASS=os.getenv("DB_PASS");DB_NAME=os.getenv("DB_NAME")
def get_conn():return pymysql.connect(host=DB_HOST,port=DB_PORT,user=DB_USER,password=DB_PASS,database=DB_NAME,cursorclass=pymysql.cursors.DictCursor,autocommit=True)
def fetchall(q,p=None):c=get_conn();r=[]; 
  ...