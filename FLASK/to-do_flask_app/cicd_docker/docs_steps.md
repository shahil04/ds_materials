To create a **Flask app ready for production**, we need to focus on **clean architecture**, **security**, **logging**, **Dockerization**, and **Gunicorn deployment**. Below is a **production-ready Flask To-Do App** setup.

---

## **1. Project Structure**

```
flask-todo/
│── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── db.py
│   └── config.py
│── templates/
│   ├── base.html
│   └── index.html
│── static/
│   └── style.css
│── tests/
│   └── test_app.py
│── wsgi.py
│── requirements.txt
│── Dockerfile
│── .dockerignore
│── .env
│── run.sh
```

---

## **2. Flask App Code**

### **app/**init**.py**

```python
from flask import Flask
from .db import init_db
from .routes import todo_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize DB
    init_db()

    # Register Blueprints
    app.register_blueprint(todo_bp)

    return app
```

---

### **app/routes.py**

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db import get_db_connection

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@todo_bp.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('task')
    if not task.strip():
        flash("Task cannot be empty!", "error")
        return redirect(url_for('todo.index'))

    conn = get_db_connection()
    conn.execute('INSERT INTO todos (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    flash("Task added successfully!", "success")
    return redirect(url_for('todo.index'))

@todo_bp.route('/update/<int:id>')
def update_task(id):
    conn = get_db_connection()
    conn.execute('UPDATE todos SET status="Completed" WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash("Task marked as completed!", "success")
    return redirect(url_for('todo.index'))

@todo_bp.route('/delete/<int:id>')
def delete_task(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id=?', (id,))
    conn.commit()
    conn.close()
    flash("Task deleted successfully!", "success")
    return redirect(url_for('todo.index'))
```

---

### **app/db.py**

```python
import sqlite3

DB_NAME = "todo.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()
```

---

### **app/config.py**

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key')
```

---

### **wsgi.py**

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

## **3. Production Requirements**

**requirements.txt**

```
Flask
gunicorn
pytest
```

---

## **4. Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]
```

---

## **5. .dockerignore**

```
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.git
tests/
```

---

## **6. Start Script**

**run.sh**

```bash
#!/bin/sh
flask db upgrade || true
exec gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

(Make it executable with `chmod +x run.sh`.)

---

## **7. Testing**

**tests/test\_app.py**

```python
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask To-Do List" in response.data
```

---

## **8. Run Locally**

```bash
docker build -t flask-todo-prod .
docker run -d -p 5000:5000 flask-todo-prod
```

---

## **9. For Real Production**

* Deploy with **NGINX + Gunicorn** (reverse proxy).
* Use **GCP, AWS, or Render** for hosting.
* Use **MySQL/Postgres** instead of SQLite for scalability.

---

# **Next Step**

Would you like me to **package this complete production-ready Flask app (with Dockerfile and tests) into a ZIP** so you can run it immediately?
