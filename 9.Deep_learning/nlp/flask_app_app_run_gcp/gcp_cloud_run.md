✅ 1. Use Google Cloud Run (Recommended Alternative)
🔹 What is Cloud Run?
A fully managed serverless platform that runs containers — you have full control over your files, Dockerfile, dependencies, and environment.

🔹 Benefits:

Files are packaged in a Docker container (you know exactly what's deployed)

Logs, scaling, custom domains — all supported

You can access Cloud Storage or Databases easily

🔹 High-level Steps:

Create Dockerfile for your Flask app

Use gcloud builds submit to deploy

Get a public URL to access

If you want, I can generate a ready-to-use Dockerfile for your current Flask app.


Here is a **complete step-by-step guide** to deploy your Flask app to **Google Cloud Run** from scratch.

---

## ✅ What You Have Locally:

Assuming you already have these files:

```
/flask_app/
│
├── app.py
├── model.pkl
├── vectorizer.pkl
├── requirements.txt
└── templates/
    └── index.html
```

---

## 🚀 Step-by-Step: Deploy Flask App on **Cloud Run**

---

### 🧱 STEP 1: **Prepare Your App**

#### ✅ 1.1 Add a `requirements.txt` (if not already)

```txt
Flask
scikit-learn
nltk
gunicorn
```

> Include any other libraries you're using.

---

#### ✅ 1.2 Create a `Dockerfile` in your `flask_app/` folder

```Dockerfile
# Use the official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Download NLTK data (optional: can package manually)
RUN python -m nltk.downloader stopwords wordnet punkt

# Expose port
EXPOSE 8080

# Start Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
```

---

### 🧪 STEP 2: Test Locally (Optional but recommended)

```bash
docker build -t my-flask-app .
docker run -p 8080:8080 my-flask-app
```

Then visit: [http://localhost:8080](http://localhost:8080)

---

### ☁️ STEP 3: Push and Deploy to Cloud Run

#### ✅ 3.1 Set GCP project and enable APIs

```bash
gcloud config set project <your-project-id>
gcloud services enable run cloudbuild containerregistry
```

#### ✅ 3.2 Authenticate if not already

```bash
gcloud auth login
gcloud auth configure-docker
```

---

#### ✅ 3.3 Deploy to Cloud Run directly (no manual Docker push needed)

```bash
gcloud run deploy flask-app \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --port 8080
```

> Choose region (like `us-central1`) and confirm prompts.

---

### ✅ STEP 4: Done — You’ll get a public URL!

Example:

```
Deployed service [flask-app] to [https://flask-app-xyz.a.run.app]
```

Open it in browser 🎉

---

## 📁 Folder Structure Summary

```
/flask_app/
│
├── app.py
├── model.pkl
├── vectorizer.pkl
├── Dockerfile
├── requirements.txt
└── templates/
    └── index.html
```

---

## 🧠 Notes

* `app.py` should expose `app = Flask(__name__)`
* Model files should load using relative paths like `model.pkl`, `vectorizer.pkl`
* HTML files must be in `templates/`
* Static files (CSS, JS) should be in `static/` if any

---

## 💬 Example `app.py` (Minimum working app)

```python
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['text']
    X = vectorizer.transform([text])
    prediction = model.predict(X)
    return render_template('index.html', prediction=prediction[0])

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 🔄 Future Updates

To redeploy after updates:

```bash
gcloud run deploy flask-app \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```
