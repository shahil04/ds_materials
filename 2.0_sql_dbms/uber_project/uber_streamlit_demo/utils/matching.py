from db import fetchall
from utils.geo_utils import haversine

def nearest_available_driver(pickup_lat, pickup_lon):
    drivers = fetchall("SELECT u.id AS user_id, u.name, d.lat, d.lon FROM users u JOIN drivers d ON u.id=d.user_id WHERE d.available=TRUE")
    best, best_dist = None, None
    for d in drivers:
        dist = haversine(pickup_lat, pickup_lon, d['lat'], d['lon'])
        if best is None or dist < best_dist:
            best, best_dist = d, dist
    return best, best_dist
