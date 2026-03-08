# app.py
import streamlit as st
from db import fetchall, fetchone, execute
import pandas as pd
import math
from datetime import datetime

st.set_page_config(page_title="Uber-like Demo", layout="wide")

# Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.asin(math.sqrt(a))

# Utility DB functions
def list_drivers():
    return fetchall("SELECT u.id as user_id, u.name, d.vehicle, d.lat, d.lon, d.available FROM users u JOIN drivers d ON u.id=d.user_id")

def list_riders():
    return fetchall("SELECT id, name, phone FROM users WHERE role='rider'")

def register_user(name, phone, role):
    return execute("INSERT INTO users (name, phone, role) VALUES (%s,%s,%s)", (name, phone, role))

def register_driver(user_id, vehicle, lat, lon):
    return execute("INSERT INTO drivers (user_id, vehicle, lat, lon, available) VALUES (%s,%s,%s,%s, True)", (user_id, vehicle, lat, lon))

def update_driver_location(user_id, lat, lon, available=True):
    return execute("UPDATE drivers SET lat=%s, lon=%s, available=%s WHERE user_id=%s", (lat, lon, available, user_id))

def create_ride(rider_id, pickup_lat, pickup_lon, drop_lat, drop_lon, fare_estimate=None):
    return execute("INSERT INTO rides (rider_id, pickup_lat, pickup_lon, drop_lat, drop_lon, fare_estimate) VALUES (%s,%s,%s,%s,%s,%s)",
                   (rider_id, pickup_lat, pickup_lon, drop_lat, drop_lon, fare_estimate))

def assign_driver_to_ride(ride_id, driver_user_id):
    execute("UPDATE rides SET driver_id=%s, accepted_at=%s, status='accepted' WHERE id=%s", (driver_user_id, datetime.now(), ride_id))
    # mark driver unavailable
    execute("UPDATE drivers SET available=FALSE WHERE user_id=%s", (driver_user_id,))

def start_ride(ride_id):
    execute("UPDATE rides SET started_at=%s, status='started' WHERE id=%s", (datetime.now(), ride_id))

def complete_ride(ride_id, fare):
    execute("UPDATE rides SET completed_at=%s, status='completed', fare_estimate=%s WHERE id=%s", (datetime.now(), fare, ride_id))
    # free driver
    r = fetchone("SELECT driver_id FROM rides WHERE id=%s", (ride_id,))
    if r and r.get("driver_id"):
        execute("UPDATE drivers SET available=TRUE WHERE user_id=%s", (r["driver_id"],))

def nearest_available_driver(pickup_lat, pickup_lon):
    drivers = fetchall("SELECT u.id AS user_id, u.name, d.lat, d.lon FROM users u JOIN drivers d ON u.id=d.user_id WHERE d.available=TRUE")
    best = None
    best_dist = None
    for d in drivers:
        dist = haversine(pickup_lat, pickup_lon, d['lat'], d['lon'])
        if best is None or dist < best_dist:
            best = d
            best_dist = dist
    return best, best_dist

# UI
st.title("Uber-like Demo (Streamlit + MySQL)")

tabs = st.tabs(["Dashboard", "Rider Flow", "Driver Flow", "Admin / Seed Data"])

# Dashboard: show drivers & active rides on map
with tabs[0]:
    st.header("Live Map & Status")
    drivers = list_drivers()
    df_drivers = pd.DataFrame(drivers)
    if not df_drivers.empty:
        st.subheader("Drivers")
        st.dataframe(df_drivers)
        # st.map wants columns named 'lat' and 'lon'
        st.map(df_drivers[['lat','lon']].dropna())

    rides = fetchall("SELECT r.*, u.name as rider_name FROM rides r JOIN users u ON r.rider_id=u.id ORDER BY r.requested_at DESC LIMIT 20")
    if rides:
        st.subheader("Recent Rides")
        st.dataframe(pd.DataFrame(rides))

with tabs[1]:
    st.header("Rider - Request a Ride")
    riders = list_riders()
    rider_map = {f"{r['name']} (id:{r['id']})": r['id'] for r in riders}
    selected = st.selectbox("Select rider (or register new)", ["-- register new --"] + list(rider_map.keys()))
    if selected == "-- register new --":
        name = st.text_input("Rider name")
        phone = st.text_input("Phone")
        if st.button("Register Rider"):
            uid = register_user(name, phone, "rider")
            execute("INSERT INTO riders (user_id, default_payment_method) VALUES (%s, %s)", (uid, "card"))
            st.success(f"Registered rider {name} with id {uid}")
    else:
        rider_id = rider_map[selected]
        st.write("Create ride request")
        col1, col2 = st.columns(2)
        with col1:
            pickup_lat = st.number_input("Pickup lat", value=28.6448, format="%.6f")
            pickup_lon = st.number_input("Pickup lon", value=77.2167, format="%.6f")
        with col2:
            drop_lat = st.number_input("Drop lat", value=28.6510, format="%.6f")
            drop_lon = st.number_input("Drop lon", value=77.2320, format="%.6f")
        if st.button("Request Ride"):
            ride_id = create_ride(rider_id, pickup_lat, pickup_lon, drop_lat, drop_lon, fare_estimate=0)
            st.success(f"Ride requested (id {ride_id}). Finding nearest driver...")
            driver, dist = nearest_available_driver(pickup_lat, pickup_lon)
            if driver:
                st.info(f"Nearest driver: {driver['name']} (id {driver['user_id']}) distance {dist:.2f} km")
                if st.button("Auto-assign nearest driver"):
                    assign_driver_to_ride(ride_id, driver['user_id'])
                    st.success("Driver assigned")
            else:
                st.warning("No available drivers right now. Try again later.")

with tabs[2]:
    st.header("Driver - Update status / Accept ride")
    # driver selection
    drivers_list = list_drivers()
    driver_map = {f"{d['name']} (id:{d['user_id']})": d['user_id'] for d in drivers_list}
    selected_driver = st.selectbox("Select driver (or register new)", ["-- register new --"] + list(driver_map.keys()))
    if selected_driver == "-- register new --":
        name = st.text_input("Driver name")
        phone = st.text_input("Phone")
        vehicle = st.text_input("Vehicle")
        lat = st.number_input("Lat", value=28.64, format="%.6f")
        lon = st.number_input("Lon", value=77.21, format="%.6f")
        if st.button("Register Driver"):
            uid = register_user(name, phone, "driver")
            register_driver(uid, vehicle, lat, lon)
            st.success(f"Registered driver {name} id {uid}")
    else:
        driver_user_id = driver_map[selected_driver]
        st.write("Update location / availability")
        lat = st.number_input("Current lat", value=28.64, format="%.6f", key="dlat")
        lon = st.number_input("Current lon", value=77.21, format="%.6f", key="dlon")
        available = st.checkbox("Available", value=True)
        if st.button("Update driver info"):
            update_driver_location(driver_user_id, lat, lon, available)
            st.success("Updated")

        st.write("Pending ride requests near you (unaccepted)")
        pending = fetchall("""SELECT r.*, u.name as rider_name FROM rides r JOIN users u ON r.rider_id=u.id
                              WHERE r.status='requested' ORDER BY r.requested_at ASC LIMIT 10""")
        if pending:
            for r in pending:
                st.write(f"Ride {r['id']} from rider {r['rider_name']} pickup ({r['pickup_lat']},{r['pickup_lon']})")
                if st.button(f"Accept ride {r['id']}", key=f"accept_{r['id']}"):
                    # accept and set driver
                    assign_driver_to_ride(r['id'], driver_user_id)
                    st.success(f"Accepted ride {r['id']}")
        else:
            st.info("No pending rides")

with tabs[3]:
    st.header("Admin / Seed actions")
    if st.button("Show DB summary"):
        users = fetchall("SELECT id,name,role FROM users")
        st.write("Users")
        st.dataframe(pd.DataFrame(users))
        st.write("Drivers")
        st.dataframe(pd.DataFrame(list_drivers()))
        st.write("Rides")
        st.dataframe(pd.DataFrame(fetchall("SELECT * FROM rides ORDER BY requested_at DESC LIMIT 50")))

    if st.button("Reset sample rides"):
        execute("DELETE FROM rides")
        st.success("Cleared rides table")

    st.markdown("**Manual complete a ride by id**")
    ride_to_complete = st.number_input("Ride id to complete", value=0, step=1)
    fare = st.number_input("Fare to apply", value=100.0)
    if st.button("Complete ride"):
        if ride_to_complete > 0:
            complete_ride(ride_to_complete, fare)
            st.success("Ride completed")

