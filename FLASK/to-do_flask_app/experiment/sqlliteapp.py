import sqlite3

# Connect to a database (creates one if not exists)
conn = sqlite3.connect("my_database.db")

print("Connected to SQLite database")

# Create a cursor object to execute SQL commands
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        );
""")
conn.commit()  # Save changes
print("Table created successfully")

cursor.execute("INSERT INTO customers (name, email, city) VALUES (?, ?, ?)",
               ("John Doe", "john@example.com", "Chicago"))
conn.commit()

cursor.execute("SELECT * FROM customers;")
rows = cursor.fetchall()  # Fetch all rows
for r in rows:
    print(r)









# import sqlite3
# from flask import g

# DATABASE = 'database.db'

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()