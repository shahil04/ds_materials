To take your **Flask + MySQL To-Do List app** to **production** with **CI/CD, Docker, and GCP**, we’ll set up a **production-grade pipeline**.

---

# **Production Deployment Plan**

## **1. Prepare Flask App for Production**

* Separate **development** and **production** configurations:

  * Use `.env` for DB credentials, secret keys, etc.
  * Use `python-dotenv` to load environment variables.

**Example `.env`:**

```
FLASK_ENV=production
SECRET_KEY=your_secret_key
DB_HOST=cloud-sql-instance
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=todo_db
```

**Update `db.py`:**

```python
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return connection
```

---

## **2. Dockerize the Flask App**

### **Step 2.1: Create `Dockerfile`**

```dockerfile
# Use Python base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8080

# Run Flask in production using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
```

### **Step 2.2: Create `requirements.txt`**

```txt
Flask
mysql-connector-python
python-dotenv
gunicorn
```

### **Step 2.3: Build & Run Docker Image**

```bash
docker build -t flask-todo .
docker run -d -p 8080:8080 flask-todo
```

---

## **3. Setup MySQL in Production**

* **Option 1:** Use **Google Cloud SQL** (recommended).
* **Option 2:** Use a Docker MySQL container:

  ```bash
  docker run --name mysql-todo -e MYSQL_ROOT_PASSWORD=your_password -e MYSQL_DATABASE=todo_db -p 3306:3306 -d mysql:8
  ```

---

## **4. CI/CD with GitHub Actions (Example)**

### **Step 4.1: Create `.github/workflows/deploy.yml`**

```yaml
name: CI/CD for Flask Todo

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Tests
        run: |
          echo "No tests yet!"

      - name: Build Docker image
        run: |
          docker build -t gcr.io/${{ secrets.GCP_PROJECT }}/flask-todo:$GITHUB_SHA .

      - name: Push Docker image to GCP
        uses: google-github-actions/auth@v1
        with:
          credentials_json: ${{ secrets.GCP_SA_KEY }}
      - name: Configure Docker for GCP
        run: gcloud auth configure-docker gcr.io
      - name: Push Image
        run: docker push gcr.io/${{ secrets.GCP_PROJECT }}/flask-todo:$GITHUB_SHA
```

---

## **5. Deploy on GCP**

You have **two main options**:

### **Option 1: Use Cloud Run (Recommended)**

1. Enable **Cloud Run** and **Artifact Registry**.
2. Push your Docker image to **GCP Artifact Registry**:

   ```bash
   gcloud builds submit --tag gcr.io/<PROJECT_ID>/flask-todo
   ```
3. Deploy:

   ```bash
   gcloud run deploy flask-todo --image gcr.io/<PROJECT_ID>/flask-todo --platform managed --region asia-south1
   ```
4. Configure environment variables (`DB_HOST`, `DB_USER`, etc.) in Cloud Run.

---

### **Option 2: Use GCE (VM)**

* Create a VM instance.
* Install Docker on the VM.
* Pull your Docker image and run it.

---

## **6. Optional Enhancements**

* **HTTPS with GCP Load Balancer or Cloud Run** (managed SSL).
* **Logging & Monitoring** (Stackdriver).
* **Auto-deployment with GitHub Actions** (CI/CD → Cloud Run).

---

# **NEXT STEP**

Would you like me to **prepare a ready-to-use `Dockerfile`, `docker-compose.yml`, and GitHub Actions CI/CD pipeline for your To-Do List project with Cloud Run deployment?**
