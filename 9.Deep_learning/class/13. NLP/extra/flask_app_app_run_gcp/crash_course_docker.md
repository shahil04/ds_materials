Here is a **Docker Crash Course** from scratch to production-level deployment, including explanations, steps, and code examples. Ideal for data scientists, developers, and DevOps learners.

---

# 🚢 Docker Crash Course: From Scratch to Production

---

## 📌 What is Docker?

Docker is a platform that uses **containers** to build, run, and manage applications. A **container** packages code, dependencies, and configuration together, ensuring consistent environments.

---

## 🧱 1. Install Docker

### ✅ Windows/Mac:

* Download from: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
* Install and restart your system
* Verify with:

```bash
docker --version
```

---

## 🐳 2. Docker Basics

### ✅ Key Terms:

| Term         | Meaning                                               |
| ------------ | ----------------------------------------------------- |
| Image        | Blueprint of a container (code + dependencies)        |
| Container    | Running instance of an image                          |
| Dockerfile   | Script to build a Docker image                        |
| Docker Hub   | Public registry for storing and sharing Docker images |
| Volume       | Persistent storage for containers                     |
| Port Binding | Maps container ports to host machine                  |

---

## 📄 3. Create a Simple Flask App with Docker

### 🗂 Project Structure:

```
flask_app/
├── app.py
├── requirements.txt
└── Dockerfile
```

### 🐍 `app.py`

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Dockerized Flask!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

### 📦 `requirements.txt`

```
flask
```

### 🐳 `Dockerfile`

```dockerfile
# Use base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose app port
EXPOSE 8080

# Start app
CMD ["python", "app.py"]
```

---

## 🔨 4. Build & Run Docker Container

### 📦 Build Docker Image

```bash
docker build -t my-flask-app .
```

### 🚀 Run Container

```bash
docker run -p 8080:8080 my-flask-app
```

Visit [http://localhost:8080](http://localhost:8080)

---

## ☁️ 5. Dockerize ML Models (with pickle)

Place `model.pkl`, `vectorizer.pkl`, etc. with `app.py`, and load inside the app like:

```python
import pickle

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
```

Make sure to include them in the `Dockerfile`'s build context (same directory).

---

## 🗃️ 6. Volumes and Data Persistence

### 📁 Bind Mount:

```bash
docker run -v "$(pwd)/data":/app/data my-flask-app
```

> Syncs local `./data` with container’s `/app/data`.

---

## 🌐 7. Networking

* `docker run -p 8080:8080` maps container port 8080 to host
* `0.0.0.0` in Flask allows access from outside the container

---

## 📦 8. Push to Docker Hub

### ✅ Login:

```bash
docker login
```

### 🏷️ Tag image:

```bash
docker tag my-flask-app yourdockerhubusername/my-flask-app
```

### ⬆️ Push image:

```bash
docker push yourdockerhubusername/my-flask-app
```

---

## 🌍 9. Deploy to Production (GCP Cloud Run)

With image already pushed:

```bash
gcloud run deploy flask-app \
  --image=yourdockerhubusername/my-flask-app \
  --platform=managed \
  --region=us-central1 \
  --allow-unauthenticated
```

---

## 🧪 10. Test Multiple Containers with Docker Compose

### 🧾 `docker-compose.yml`

```yaml
version: "3.9"
services:
  web:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - .:/app
```

```bash
docker-compose up
```

---

## 🛡️ 11. Best Practices

* Use `.dockerignore` like `.gitignore`
* Minimize layers in `Dockerfile`
* Use multistage builds for production
* Never store secrets inside image

---

## 📌 Summary Cheatsheet

| Command                         | Description                     |
| ------------------------------- | ------------------------------- |
| `docker build -t <image> .`     | Build image                     |
| `docker run -p 8080:80 <image>` | Run container with port binding |
| `docker ps`                     | List running containers         |
| `docker stop <container_id>`    | Stop container                  |
| `docker exec -it <id> bash`     | Access container shell          |
| `docker images`                 | List local images               |
| `docker rmi <image>`            | Remove image                    |
| `docker login`                  | Authenticate to Docker Hub      |
| `docker push`                   | Push image to Docker Hub        |

---

Would you like this in a downloadable `README.md` format or as a GitHub-ready starter template?
