Perfect 👍 — since your **Learning Management System (LMS)** uses **Django (DRF) + PostgreSQL + React**, let’s go step-by-step to set it up **from scratch on your local system** (works on Windows, macOS, or Linux).

---

## 🧩 1. Folder structure

Create a parent project folder:

```bash
mkdir lms-project && cd lms-project
```

Inside it, create two main folders:

```bash
mkdir backend frontend
```

---

## ⚙️ 2. Setup Backend (Django + DRF + PostgreSQL)

### Step 2.1 — Create virtual environment & install dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate        # (Windows: venv\Scripts\activate)
pip install django djangorestframework psycopg2-binary djangorestframework-simplejwt django-cors-headers
```

### Step 2.2 — Create Django project

```bash
django-admin startproject lms_backend .
```

### Step 2.3 — Create apps

```bash
python manage.py startapp users
python manage.py startapp courses
```

### Step 2.4 — Add apps to `INSTALLED_APPS` in `lms_backend/settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'users',
    'courses',
]
```

### Step 2.5 — Add database configuration (PostgreSQL)

Create a database and user in PostgreSQL:

```sql
CREATE DATABASE lms_db;
CREATE USER lms_user WITH PASSWORD 'lms_pass';
ALTER ROLE lms_user SET client_encoding TO 'utf8';
ALTER ROLE lms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE lms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE lms_db TO lms_user;
```

Now update `DATABASES` in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'lms_db',
        'USER': 'lms_user',
        'PASSWORD': 'lms_pass',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🔐 3. Configure authentication (JWT)

Install package (if not already):

```bash
pip install djangorestframework-simplejwt
```

Add in `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

Add URLs in `lms_backend/urls.py`:

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

## 🧱 4. Add CORS headers for React frontend

Install:

```bash
pip install django-cors-headers
```

Add to `INSTALLED_APPS`:

```python
'corsheaders',
```

Add middleware at the top:

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    ...
]
```

Allow all origins (for development):

```python
CORS_ALLOW_ALL_ORIGINS = True
```

---

## 📦 5. Migrate and create superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Then run:

```bash
python manage.py runserver
```

✅ Backend should now run at `http://127.0.0.1:8000`

---

## ⚛️ 6. Setup Frontend (React)

Open new terminal in `frontend` folder:

```bash
cd ../frontend
npx create-react-app .
```

or (faster alternative):

```bash
npm create vite@latest .
```

Install axios & react-router:

```bash
npm install axios react-router-dom
```

Create `.env`:

```
REACT_APP_API_URL=http://127.0.0.1:8000/api
```

Then create components:

* `src/api.js` → Axios config
* `src/components/Login.js`
* `src/components/CourseList.js`
* `src/components/CourseDetail.js`

(Use the exact code from the scaffold document.)

Run the app:

```bash
npm start
```

✅ Frontend now runs at `http://localhost:3000`

---

## 🧪 7. Test full flow

1. Register or create a user in Django admin.
2. Login through `/api/token/` or frontend login page.
3. View course list → click → enroll → view lessons.

---

## 🐳 8. (Optional) Run via Docker

If you want a one-command setup:

```bash
docker-compose up --build
```

(make sure you have the `docker-compose.yml` provided in the document)

---

## ✅ You’re done!

You now have:

* **Backend:** Django REST API at `http://127.0.0.1:8000/api/`
* **Frontend:** React UI at `http://localhost:3000`
* **Database:** PostgreSQL (local or Docker)

---

Would you like me to generate:

* 🧾 A **`setup.sh`** script to automate all these steps
  **or**
* 🐳 A **Docker Compose** that includes backend + frontend + Postgres + Nginx (for production)?



=====================================
Perfect ✅ — here’s the **recommended `requirements.txt`** for your **LMS (Django + DRF + PostgreSQL + JWT + CORS)** project, aligned with the stable 2025 stack (Python 3.11/3.12 + Django 5.1):

---

### 📄 **`requirements.txt`**

```
# Core Framework
Django>=5.1,<5.2

# REST API
djangorestframework>=3.15,<3.16
djangorestframework-simplejwt>=5.3,<5.4

# Database Driver
psycopg2-binary>=2.9,<3.0

# CORS Headers (for React frontend integration)
django-cors-headers>=4.3,<4.4

# Environment Variable Management (optional but recommended)
python-dotenv>=1.0,<1.1

# Optional: For better performance and security
gunicorn>=22.0,<23.0        # For production server
whitenoise>=6.7,<6.8        # For static file serving in production
```

---

### ✅ To install all dependencies:

```bash
pip install -r requirements.txt
```

---

### ⚙️ Optional: For development Docker environment

If you plan to use Docker, you can add these too:

```
# Docker support (optional)
dj-database-url>=2.2,<2.3
```

---

### 💡 Notes:

* This stack is **compatible with PostgreSQL 15/16**.
* You can also install `ipython` and `black` for development convenience:

  ```
  ipython
  black
  ```

---

Would you like me to also generate a **`dev-requirements.txt`** (with testing tools like pytest, coverage, black, flake8) alongside this production one?
