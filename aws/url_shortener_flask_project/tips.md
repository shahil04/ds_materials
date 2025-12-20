Perfect 👍
We’ll do this in **two clean phases**, exactly how it’s done in **real projects**.

---

# 🔹 PHASE 1: Run URL Shortener **LOCALLY** (First Priority)

We will use:

* **Flask**
* **Local MySQL**
* **PyMySQL** (Windows-friendly)

---

## ✅ Step 1: Install Required Packages

```bash
pip install flask pymysql
```

---

## ✅ Step 2: Start MySQL (XAMPP / MySQL Server)

Make sure **MySQL is running**
(Default port: `3306`)

---

## ✅ Step 3: Create Database & Table

Open **MySQL Command Line / Workbench** and run:

```sql
CREATE DATABASE url_db;
USE url_db;

CREATE TABLE urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    short_code VARCHAR(10) UNIQUE,
    long_url TEXT NOT NULL,
    click_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ✅ Step 4: Update Your Flask App (LOCAL VERSION)

### 🔁 Replace entire DB section with this

```python
from flask import Flask, request, redirect, render_template
import string, random
import pymysql

app = Flask(__name__)

# LOCAL DB CONFIG
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_mysql_password"
DB_NAME = "url_db"

def get_db():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
```

---

## ✅ Step 5: Fix Cursor Usage (IMPORTANT)

### Update insert logic

```python
cur.execute(
    "INSERT INTO urls (short_code, long_url) VALUES (%s, %s)",
    (code, long_url)
)
```

### Update redirect logic

```python
result = cur.fetchone()

if result:
    cur.execute(
        "UPDATE urls SET click_count = click_count + 1 WHERE short_code=%s",
        (code,)
    )
    db.commit()
    return redirect(result["long_url"])
```

---

## ✅ Step 6: Run Flask App

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

✅ Paste a long URL
✅ Get short URL
✅ Click → redirect works
✅ DB click count increases

---

## 🟢 PHASE 1 DONE

Once this works locally → **DO NOT CHANGE CODE LOGIC AGAIN**

---

# 🔹 PHASE 2: Move from LOCAL → AWS RDS (Production)

Now we **only change DB config**, nothing else.

---

## ✅ Step 7: Create AWS RDS (MySQL)

1. AWS Console → **RDS**
2. Create database
3. Engine: **MySQL**
4. Templates: **Free tier**
5. DB name: `url_db`
6. Username: `admin`
7. Password: set your own
8. Public access: **YES**
9. VPC security group → allow **port 3306**

---

## ✅ Step 8: Get RDS Endpoint

You’ll see something like:

```
url-db.c7a9abcd1234.ap-south-1.rds.amazonaws.com
```

---

## ✅ Step 9: Create Table in RDS

Use **MySQL Workbench**
Connect using:

* Host: RDS endpoint
* Port: 3306
* Username/password

Run SAME SQL:

```sql
USE url_db;

CREATE TABLE urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    short_code VARCHAR(10) UNIQUE,
    long_url TEXT NOT NULL,
    click_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## ✅ Step 10: Switch DB Config to RDS (ONLY THIS CHANGE)

```python
DB_HOST = "url-db.c7a9abcd1234.ap-south-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "your_rds_password"
DB_NAME = "url_db"
```

Restart Flask.

🎉 **Your app is now using AWS RDS**

---

# 🔐 BEST PRACTICE (IMPORTANT)

Instead of hardcoding credentials:

```python
import os

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
```

Set env vars locally & on EC2 later.

---

## 🚀 NEXT REAL-WORLD UPGRADES (Optional)

When you’re ready, I can help you with:

* Dockerizing this app
* EC2 + Nginx + Gunicorn
* Custom domain + HTTPS
* Analytics dashboard
* Short URL expiry
* QR code generation

---

### ✅ Tell me once **LOCAL version works**

Next step → **deploy on EC2 + connect RDS like Bitly**
