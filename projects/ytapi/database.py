import sqlite3

def get_connection():
    conn = sqlite3.connect("youtube_courses.db")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for playlists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_id TEXT UNIQUE,
            playlist_name TEXT,
            youtube_link TEXT,
            extract_link TEXT,
            batch TEXT
        )
    """)
    
    # Table for courses (manual mapping)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT,
            youtube_link TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def insert_playlist(playlist_id, playlist_name, youtube_link, extract_link, batch):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO playlists (playlist_id, playlist_name, youtube_link, extract_link, batch)
        VALUES (?, ?, ?, ?, ?)
    """, (playlist_id, playlist_name, youtube_link, extract_link, batch))
    conn.commit()
    conn.close()

def insert_course(course_name, youtube_link):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO courses (course_name, youtube_link)
        VALUES (?, ?)
    """, (course_name, youtube_link))
    conn.commit()
    conn.close()

def fetch_playlists():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM playlists")
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_courses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    conn.close()
    return data


