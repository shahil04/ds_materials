# 1. Create MySQL DB and Tables
mysql -u root -p < schema.sql

# 2. Install Python packages
pip install streamlit mysql-connector-python

# 3. Run the Streamlit App
streamlit run app.py




---

## 🚖 Project: Uber Booking System (Demo)

### 🧩 Tech Stack

* **Frontend:** Streamlit
* **Backend Database:** MySQL
* **Python Connector:** `mysql-connector-python`

---

## 🗂 Database Schema (from your image)

We'll use the following tables:

```sql
CREATE DATABASE uber_demo;
USE uber_demo;

CREATE TABLE customers (
  customer_id TEXT PRIMARY KEY,
  name TEXT,
  phone BIGINT,
  email TEXT,
  join_date TEXT
);

CREATE TABLE drivers (
  driver_id TEXT PRIMARY KEY,
  name TEXT,
  phone BIGINT,
  rating DOUBLE
);

CREATE TABLE cabs (
  cab_id TEXT PRIMARY KEY,
  vehicle_type TEXT,
  registration_no TEXT,
  driver_id TEXT,
  FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
);

CREATE TABLE bookings (
  booking_id VARCHAR(100) PRIMARY KEY,
  customer_id TEXT,
  cab_id TEXT,
  booking_time TEXT,
  pickup_location TEXT,
  dropoff_location TEXT,
  status TEXT,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (cab_id) REFERENCES cabs(cab_id)
);

CREATE TABLE trip_details (
  trip_id VARCHAR(100) PRIMARY KEY,
  booking_id VARCHAR(100),
  start_time TEXT,
  end_time TEXT,
  distance_km DOUBLE,
  fare DOUBLE,
  FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);

CREATE TABLE feedback (
  feedback_id TEXT PRIMARY KEY,
  booking_id TEXT,
  customer_rating TEXT,
  driver_rating TEXT,
  cancellation_reason TEXT,
  FOREIGN KEY (booking_id) REFERENCES bookings(booking_id)
);
```

---

## 📁 Folder Structure

```
uber_booking_system/
│
├── app.py
├── requirements.txt
└── db_config.py
```

---

## ⚙️ `db_config.py`

```python
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="uber_demo"
    )
```

---

## 🎨 `app.py` (Streamlit App)

```python
import streamlit as st
import mysql.connector
from db_config import get_connection
import uuid
from datetime import datetime

st.set_page_config(page_title="Uber Booking System", layout="wide")

# Navigation menu
menu = ["Home", "Add Customer", "Book Ride", "View Bookings", "Trip Details", "Feedback"]
choice = st.sidebar.selectbox("Menu", menu)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

# Home
if choice == "Home":
    st.title("🚖 Uber Booking System Demo")
    st.markdown("""
    ### Features:
    - Add new customers  
    - Book a cab ride  
    - View and update bookings  
    - Add feedback for completed trips  
    """)

# Add Customer
elif choice == "Add Customer":
    st.header("Add New Customer")
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")

    if st.button("Add Customer"):
        cust_id = str(uuid.uuid4())[:8]
        join_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "INSERT INTO customers VALUES (%s,%s,%s,%s,%s)",
            (cust_id, name, phone, email, join_date)
        )
        conn.commit()
        st.success(f"Customer {name} added successfully!")

# Book Ride
elif choice == "Book Ride":
    st.header("Book a Ride")
    cursor.execute("SELECT customer_id, name FROM customers")
    customers = cursor.fetchall()
    customer_dict = {c['name']: c['customer_id'] for c in customers}

    cursor.execute("SELECT cab_id, vehicle_type FROM cabs")
    cabs = cursor.fetchall()
    cab_dict = {c['vehicle_type']: c['cab_id'] for c in cabs}

    customer_name = st.selectbox("Customer", list(customer_dict.keys()))
    cab_type = st.selectbox("Cab Type", list(cab_dict.keys()))
    pickup = st.text_input("Pickup Location")
    dropoff = st.text_input("Drop-off Location")
    status = st.selectbox("Status", ["Booked", "Completed", "Cancelled"])

    if st.button("Confirm Booking"):
        booking_id = str(uuid.uuid4())[:8]
        booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO bookings VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (booking_id, customer_dict[customer_name], cab_dict[cab_type],
             booking_time, pickup, dropoff, status)
        )
        conn.commit()
        st.success(f"Booking confirmed! Booking ID: {booking_id}")

# View Bookings
elif choice == "View Bookings":
    st.header("All Bookings")
    cursor.execute("""
        SELECT b.booking_id, c.name AS customer, cb.vehicle_type, b.pickup_location, 
               b.dropoff_location, b.status
        FROM bookings b
        JOIN customers c ON b.customer_id=c.customer_id
        JOIN cabs cb ON b.cab_id=cb.cab_id
    """)
    data = cursor.fetchall()
    st.dataframe(data)

# Trip Details
elif choice == "Trip Details":
    st.header("Add Trip Details")
    cursor.execute("SELECT booking_id FROM bookings WHERE status='Completed'")
    bookings = cursor.fetchall()
    booking_id = st.selectbox("Booking ID", [b['booking_id'] for b in bookings])

    start = st.text_input("Start Time")
    end = st.text_input("End Time")
    distance = st.number_input("Distance (km)", min_value=0.0)
    fare = st.number_input("Fare (₹)", min_value=0.0)

    if st.button("Add Trip"):
        trip_id = str(uuid.uuid4())[:8]
        cursor.execute(
            "INSERT INTO trip_details VALUES (%s,%s,%s,%s,%s,%s)",
            (trip_id, booking_id, start, end, distance, fare)
        )
        conn.commit()
        st.success(f"Trip details added for booking {booking_id}")

# Feedback
elif choice == "Feedback":
    st.header("Customer Feedback")
    cursor.execute("SELECT booking_id FROM bookings")
    bookings = cursor.fetchall()
    booking_id = st.selectbox("Booking ID", [b['booking_id'] for b in bookings])

    customer_rating = st.slider("Customer Rating", 1, 5)
    driver_rating = st.slider("Driver Rating", 1, 5)
    reason = st.text_area("Cancellation Reason (if any)")

    if st.button("Submit Feedback"):
        feedback_id = str(uuid.uuid4())[:8]
        cursor.execute(
            "INSERT INTO feedback VALUES (%s,%s,%s,%s,%s)",
            (feedback_id, booking_id, customer_rating, driver_rating, reason)
        )
        conn.commit()
        st.success("Feedback submitted successfully!")
```

---

## 📦 `requirements.txt`

```
streamlit
mysql-connector-python
```

---

## ▶️ Run Instructions

```bash
# 1. Create MySQL DB and Tables
mysql -u root -p < schema.sql

# 2. Install Python packages
pip install streamlit mysql-connector-python

# 3. Run the Streamlit App
streamlit run app.py
```

---

## 🧠 Features You Can Extend

* Add driver login and cab assignment dashboard
* Add fare calculation based on distance (auto formula)
* Integrate Google Maps API for route and distance
* Display real-time trip tracking simulation

---

Would you like me to **generate a downloadable ZIP** with all code files (`app.py`, `db_config.py`, `requirements.txt`, and schema.sql`)?
