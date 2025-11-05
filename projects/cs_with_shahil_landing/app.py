
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'dev-secret-key')

def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-enquiry', methods=['POST'])
def submit_enquiry():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    mobile = data.get('mobile')
    course = data.get('course')
    message = data.get('message')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO enquiries (name, email, mobile, course, message)
            VALUES (%s, %s, %s, %s, %s)""", (name, email, mobile, course, message)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Enquiry submitted successfully!', 'success')
        return redirect(url_for('index'))
    except Error as e:
        print('DB Error:', e)
        flash('There was a server error. Please try again later.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
