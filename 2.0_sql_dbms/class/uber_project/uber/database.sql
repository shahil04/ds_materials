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
