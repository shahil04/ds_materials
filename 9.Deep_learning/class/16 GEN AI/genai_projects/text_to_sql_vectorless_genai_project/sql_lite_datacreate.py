import sqlite3
import random
from datetime import datetime, timedelta

# ----------------------------------
# Create Database
# ----------------------------------
conn = sqlite3.connect("uber.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# ----------------------------------
# Drop Existing Tables
# ----------------------------------
tables = [
    "trip_details",
    "feedback",
    "bookings",
    "trip_requests",
    "customers",
    "cabs",
    "drivers"
]

for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# ----------------------------------
# Create Tables
# ----------------------------------

cursor.execute("""
CREATE TABLE customers(
    customer_id TEXT PRIMARY KEY,
    name TEXT,
    phone INTEGER,
    email TEXT,
    join_date TEXT
)
""")

cursor.execute("""
CREATE TABLE drivers(
    driver_id TEXT PRIMARY KEY,
    name TEXT,
    phone INTEGER,
    rating REAL
)
""")

cursor.execute("""
CREATE TABLE cabs(
    cab_id TEXT PRIMARY KEY,
    vehicle_type TEXT,
    registration_no TEXT,
    driver_id TEXT,
    FOREIGN KEY(driver_id) REFERENCES drivers(driver_id)
)
""")

cursor.execute("""
CREATE TABLE bookings(
    booking_id TEXT PRIMARY KEY,
    customer_id TEXT,
    cab_id TEXT,
    booking_time TEXT,
    pickup_location TEXT,
    dropoff_location TEXT,
    status TEXT,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
)
""")

cursor.execute("""
CREATE TABLE feedback(
    feedback_id TEXT PRIMARY KEY,
    booking_id TEXT,
    customer_rating TEXT,
    driver_rating TEXT,
    cancellation_reason TEXT,
    FOREIGN KEY(booking_id) REFERENCES bookings(booking_id)
)
""")

cursor.execute("""
CREATE TABLE trip_details(
    trip_id TEXT PRIMARY KEY,
    booking_id TEXT,
    start_time TEXT,
    end_time TEXT,
    distance_km REAL,
    fare REAL,
    FOREIGN KEY(booking_id) REFERENCES bookings(booking_id)
)
""")

cursor.execute("""
CREATE TABLE trip_requests(
    request_id INTEGER PRIMARY KEY,
    pickup_location TEXT,
    dropoff_location TEXT,
    request_time TEXT
)
""")

# ----------------------------------
# Dummy Data
# ----------------------------------

customer_names = [
    "Rahul","Amit","Priya","Sneha","Anjali","Neha","Rohit","Karan",
    "Pooja","Riya","Vikram","Arjun","Mohit","Sahil","Nisha",
    "Ankit","Ramesh","Suresh","Deepak","Ayesha"
]

driver_names = [
    "Rakesh","Manoj","Sunil","Akash","Rajesh","Sanjay","Mahesh",
    "Lokesh","Imran","Aslam","Salman","Harish","Prakash",
    "Naresh","Mukesh"
]

locations = [
    "Connaught Place",
    "Noida Sector 18",
    "Gurgaon Cyber Hub",
    "Dwarka",
    "Karol Bagh",
    "Rohini",
    "Lajpat Nagar",
    "Saket",
    "Janakpuri",
    "Airport T3"
]

vehicle_types = [
    "Mini",
    "Sedan",
    "SUV",
    "Auto",
    "Bike"
]

statuses = [
    "Completed",
    "Cancelled",
    "Ongoing"
]

cancel_reasons = [
    None,
    None,
    None,
    "Driver Cancelled",
    "Customer Cancelled",
    "No Driver Available",
    "Payment Issue"
]

# ----------------------------------
# Insert Customers
# ----------------------------------

customer_ids = []

for i in range(1, 51):
    cid = f"CUST{i:03}"
    customer_ids.append(cid)

    cursor.execute("""
    INSERT INTO customers VALUES(?,?,?,?,?)
    """, (
        cid,
        random.choice(customer_names),
        random.randint(9000000000,9999999999),
        f"user{i}@gmail.com",
        (datetime.now()-timedelta(days=random.randint(30,1000))).strftime("%Y-%m-%d")
    ))

# ----------------------------------
# Insert Drivers
# ----------------------------------

driver_ids=[]

for i in range(1,21):

    did=f"DRV{i:03}"
    driver_ids.append(did)

    cursor.execute("""
    INSERT INTO drivers VALUES(?,?,?,?)
    """,(
        did,
        random.choice(driver_names),
        random.randint(9000000000,9999999999),
        round(random.uniform(3.5,5.0),1)
    ))

# ----------------------------------
# Insert Cabs
# ----------------------------------

cab_ids=[]

for i in range(1,21):

    cab=f"CAB{i:03}"
    cab_ids.append(cab)

    cursor.execute("""
    INSERT INTO cabs VALUES(?,?,?,?)
    """,(
        cab,
        random.choice(vehicle_types),
        f"DL01AB{i:04}",
        random.choice(driver_ids)
    ))

# ----------------------------------
# Insert Bookings
# ----------------------------------

booking_ids=[]

for i in range(1,51):

    bid=f"BOOK{i:03}"
    booking_ids.append(bid)

    booking_time=datetime.now()-timedelta(days=random.randint(1,60))

    cursor.execute("""
    INSERT INTO bookings VALUES(?,?,?,?,?,?,?)
    """,(
        bid,
        random.choice(customer_ids),
        random.choice(cab_ids),
        booking_time.strftime("%Y-%m-%d %H:%M:%S"),
        random.choice(locations),
        random.choice(locations),
        random.choice(statuses)
    ))

# ----------------------------------
# Feedback
# ----------------------------------

for i,bid in enumerate(booking_ids,1):

    cursor.execute("""
    INSERT INTO feedback VALUES(?,?,?,?,?)
    """,(
        f"FB{i:03}",
        bid,
        str(random.randint(1,5)),
        str(random.randint(1,5)),
        random.choice(cancel_reasons)
    ))

# ----------------------------------
# Trip Details
# ----------------------------------

for i,bid in enumerate(booking_ids,1):

    start=datetime.now()-timedelta(days=random.randint(1,30))
    end=start+timedelta(minutes=random.randint(10,90))

    distance=round(random.uniform(2,35),2)
    fare=round(distance*18+random.randint(30,120),2)

    cursor.execute("""
    INSERT INTO trip_details VALUES(?,?,?,?,?,?)
    """,(
        f"TRIP{i:03}",
        bid,
        start.strftime("%Y-%m-%d %H:%M:%S"),
        end.strftime("%Y-%m-%d %H:%M:%S"),
        distance,
        fare
    ))

# ----------------------------------
# Trip Requests
# ----------------------------------

for i in range(1,51):

    cursor.execute("""
    INSERT INTO trip_requests VALUES(?,?,?,?)
    """,(
        i,
        random.choice(locations),
        random.choice(locations),
        (datetime.now()-timedelta(days=random.randint(1,30))).strftime("%Y-%m-%d %H:%M:%S")
    ))

conn.commit()

# ----------------------------------
# Verify Records
# ----------------------------------

tables = [
    "customers",
    "drivers",
    "cabs",
    "bookings",
    "feedback",
    "trip_details",
    "trip_requests"
]

print("\nDatabase Created Successfully!\n")

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"{table:15} -> {cursor.fetchone()[0]} records")

conn.close()

print("\nuber.db created successfully.")



# =============================
#==============================
