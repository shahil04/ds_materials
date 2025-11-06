import streamlit as st
import uuid
from datetime import datetime
from db_config import get_connection

st.set_page_config(page_title="Uber Booking System", layout="wide")

def init_data():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM drivers")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO drivers VALUES ('d1','Amit','9999999999',4.8)")
        cursor.execute("INSERT INTO drivers VALUES ('d2','Neha','8888888888',4.5)")
        cursor.execute("INSERT INTO drivers VALUES ('d3','Ravi','7777777777',4.9)")

    cursor.execute("SELECT COUNT(*) FROM cabs")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO cabs VALUES ('c1','Sedan','UP14AB1234','d1')")
        cursor.execute("INSERT INTO cabs VALUES ('c2','SUV','DL1CAB5678','d2')")
        cursor.execute("INSERT INTO cabs VALUES ('c3','Mini','UP16XYZ9876','d3')")
    conn.commit()
    conn.close()

init_data()

menu = ["Home", "Register Customer", "Book a Cab", "View Bookings", "Feedback"]
choice = st.sidebar.radio("Menu", menu)

conn = get_connection()
cursor = conn.cursor(dictionary=True)

# HOME PAGE
if choice == "Home":
    st.title("🚖 Uber Booking System (Demo)")
    st.markdown("""
    ### 🧭 Features
    - Register new customers  
    - Book a ride  
    - View booking history  
    - Add feedback after rides  
    """)

# REGISTER CUSTOMER
elif choice == "Register Customer":
    st.header("Register a New Customer")
    name = st.text_input("Full Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    if st.button("Register"):
        customer_id = str(uuid.uuid4())[:8]
        join_date = datetime.now().date()
        cursor.execute(
            "INSERT INTO customers VALUES (%s,%s,%s,%s,%s)",
            (customer_id, name, phone, email, join_date)
        )
        conn.commit()
        st.success(f"Customer {name} registered successfully!")

# BOOK A CAB
elif choice == "Book a Cab":
    st.header("Book a Cab Ride")

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    if not customers:
        st.warning("⚠️ Please register a customer first!")
    else:
        customer = st.selectbox("Select Customer", [c["name"] for c in customers])
        customer_id = [c["customer_id"] for c in customers if c["name"] == customer][0]

        cursor.execute("""
            SELECT c.cab_id, c.vehicle_type, d.name AS driver_name, d.rating 
            FROM cabs c JOIN drivers d ON c.driver_id=d.driver_id
        """)
        cabs = cursor.fetchall()

        st.write("### 🚗 Available Cabs:")
        for cab in cabs:
            st.info(f"{cab['vehicle_type']} - Driver: {cab['driver_name']} (⭐ {cab['rating']})")

        cab_type = st.selectbox("Select Cab Type", [c["vehicle_type"] for c in cabs])
        pickup = st.text_input("Pickup Location")
        dropoff = st.text_input("Drop-off Location")

        if st.button("Confirm Booking"):
            cab_id = [c["cab_id"] for c in cabs if c["vehicle_type"] == cab_type][0]
            booking_id = str(uuid.uuid4())[:8]
            booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("""
                INSERT INTO bookings VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (booking_id, customer_id, cab_id, booking_time, pickup, dropoff, "Booked"))
            conn.commit()
            st.success(f"✅ Booking confirmed! Booking ID: {booking_id}")

# VIEW BOOKINGS
elif choice == "View Bookings":
    st.header("📋 Booking History")
    cursor.execute("""
        SELECT b.booking_id, c.name AS customer, cb.vehicle_type, 
               b.pickup_location, b.dropoff_location, b.status, b.booking_time
        FROM bookings b
        JOIN customers c ON b.customer_id=c.customer_id
        JOIN cabs cb ON b.cab_id=cb.cab_id
        ORDER BY b.booking_time DESC
    """)
    data = cursor.fetchall()
    if data:
        st.dataframe(data)
    else:
        st.info("No bookings found.")

# FEEDBACK
elif choice == "Feedback":
    st.header("💬 Customer Feedback")
    cursor.execute("SELECT booking_id FROM bookings")
    bookings = [b["booking_id"] for b in cursor.fetchall()]

    if bookings:
        booking_id = st.selectbox("Booking ID", bookings)
        cust_rating = st.slider("Customer Rating", 1, 5)
        driver_rating = st.slider("Driver Rating", 1, 5)
        reason = st.text_area("Cancellation Reason (optional)")
        if st.button("Submit Feedback"):
            feedback_id = str(uuid.uuid4())[:8]
            cursor.execute(
                "INSERT INTO feedback VALUES (%s,%s,%s,%s,%s)",
                (feedback_id, booking_id, cust_rating, driver_rating, reason)
            )
            conn.commit()
            st.success("Feedback submitted successfully!")
    else:
        st.warning("No bookings available for feedback.")

conn.close()
