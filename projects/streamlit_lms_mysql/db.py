
import mysql.connector
from mysql.connector import errorcode
from config import DB_CONFIG
import hashlib

def get_connection(require_db=True):
    cfg = DB_CONFIG.copy()
    if not require_db:
        # connect without database (for create)
        cfg2 = cfg.copy()
        cfg2.pop("database", None)
        return mysql.connector.connect(**cfg2)
    return mysql.connector.connect(**cfg)

def create_database_and_tables():
    # Create database and required tables if they don't exist
    cnx = get_connection(require_db=False)
    cursor = cnx.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS `{}` DEFAULT CHARACTER SET 'utf8'".format(DB_CONFIG["database"]))
    except Exception as e:
        print("Could not create database:", e)
    finally:
        cursor.close()
        cnx.close()

    cnx = get_connection()
    cursor = cnx.cursor()
    # tables
    tables = {}
    tables['users'] = (
        "CREATE TABLE IF NOT EXISTS users ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  username VARCHAR(100) NOT NULL UNIQUE,"
        "  email VARCHAR(255) NOT NULL,"
        "  password VARCHAR(255) NOT NULL"
        ") ENGINE=InnoDB")
    tables['courses'] = (
        "CREATE TABLE IF NOT EXISTS courses ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  title VARCHAR(255) NOT NULL,"
        "  slug VARCHAR(255) NOT NULL,"
        "  description TEXT,"
        "  thumbnail VARCHAR(255)"
        ") ENGINE=InnoDB")
    tables['modules'] = (
        "CREATE TABLE IF NOT EXISTS modules ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  course_id INT NOT NULL,"
        "  title VARCHAR(255) NOT NULL,"
        "  ordering INT DEFAULT 0,"
        "  FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE"
        ") ENGINE=InnoDB")
    tables['videos'] = (
        "CREATE TABLE IF NOT EXISTS videos ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  module_id INT NOT NULL,"
        "  title VARCHAR(255) NOT NULL,"
        "  youtube_link TEXT,"
        "  ordering INT DEFAULT 0,"
        "  FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE"
        ") ENGINE=InnoDB")
    tables['progress'] = (
        "CREATE TABLE IF NOT EXISTS progress ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  user_id INT NOT NULL,"
        "  video_id INT NOT NULL,"
        "  completed BOOLEAN DEFAULT FALSE,"
        "  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        "  UNIQUE KEY (user_id, video_id),"
        "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,"
        "  FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE"
        ") ENGINE=InnoDB")
    tables['notes'] = (
        "CREATE TABLE IF NOT EXISTS notes ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  user_id INT NOT NULL,"
        "  video_id INT NOT NULL,"
        "  note TEXT,"
        "  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,"
        "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,"
        "  FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE"
        ") ENGINE=InnoDB")
    tables['ratings'] = (
        "CREATE TABLE IF NOT EXISTS ratings ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  user_id INT NOT NULL,"
        "  video_id INT NOT NULL,"
        "  rating INT,"
        "  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
        "  UNIQUE KEY (user_id, video_id),"
        "  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,"
        "  FOREIGN KEY (video_id) REFERENCES videos(id) ON DELETE CASCADE"
        ") ENGINE=InnoDB")

    for name, ddl in tables.items():
        try:
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            print(err.msg)
    cnx.commit()
    cursor.close()
    cnx.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, email, password):
    cnx = get_connection()
    cursor = cnx.cursor()
    pw = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, pw))
        cnx.commit()
        return True, None
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close(); cnx.close()

def authenticate(username, password):
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    row = cursor.fetchone()
    cursor.close(); cnx.close()
    if not row:
        return None
    if row["password"] == hash_password(password):
        return row
    return None

def seed_demo_data():
    cnx = get_connection()
    cursor = cnx.cursor()
    # check if courses exist
    cursor.execute("SELECT COUNT(*) FROM courses")
    if cursor.fetchone()[0] > 0:
        cursor.close(); cnx.close(); return
    # insert courses
    courses = [
        ("Python Full Stack","python-full-stack","Learn Python end-to-end","assets/python.jpg"),
        ("Java Full Stack","java-full-stack","Become a Java developer","assets/java.jpg"),
        ("Data Science Pro","data-science-pro","Master data science workflows","assets/data_science.jpg"),
        ("AI / ML Foundation","ai-ml-foundation","Intro to AI & ML","assets/ai_ml.jpg"),
    ]
    cursor.executemany("INSERT INTO courses (title, slug, description, thumbnail) VALUES (%s,%s,%s,%s)", courses)
    cnx.commit()
    # modules & videos (simple hardcoded demo)
    cursor.execute("SELECT id FROM courses")
    course_ids = [r[0] for r in cursor.fetchall()]
    for cid in course_ids:
        # add 2 modules each
        cursor.execute("INSERT INTO modules (course_id, title, ordering) VALUES (%s,%s,%s)", (cid, "Module 01", 1))
        m1 = cursor.lastrowid
        cursor.execute("INSERT INTO modules (course_id, title, ordering) VALUES (%s,%s,%s)", (cid, "Module 02", 2))
        m2 = cursor.lastrowid
        # add 2 demo videos per module (public youtube example links)
        cursor.execute("INSERT INTO videos (module_id, title, youtube_link, ordering) VALUES (%s,%s,%s,%s)",
                       (m1, "Welcome & Introduction", "https://www.youtube.com/watch?v=YS4e4q9oBaU", 1))
        cursor.execute("INSERT INTO videos (module_id, title, youtube_link, ordering) VALUES (%s,%s,%s,%s)",
                       (m1, "Getting Started", "https://www.youtube.com/watch?v=rfscVS0vtbw", 2))
        cursor.execute("INSERT INTO videos (module_id, title, youtube_link, ordering) VALUES (%s,%s,%s,%s)",
                       (m2, "Deep Dive - Part 1", "https://www.youtube.com/watch?v=VAcKXS_V_Kc", 1))
        cursor.execute("INSERT INTO videos (module_id, title, youtube_link, ordering) VALUES (%s,%s,%s,%s)",
                       (m2, "Deep Dive - Part 2", "https://www.youtube.com/watch?v=H1elmMBnykA", 2))
    cnx.commit()
    cursor.close(); cnx.close()
