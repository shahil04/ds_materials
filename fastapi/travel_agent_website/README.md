# PeaceTimeTravellers

AI-powered travel platform (React + FastAPI + MySQL + RAG + Docker + GitHub Actions)

## Setup

1. Copy `.env` and adjust values.
2. Setup MySQL (or docker-compose will do it).

### Run with docker-compose

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs

### Local backend (without Docker)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Local frontend development

```bash
cd frontend
npm install
npm run dev
```

## API endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/packages`
- `POST /api/packages`
- `PUT /api/packages/{id}`
- `DELETE /api/packages/{id}`
- `POST /api/generate-itinerary`
- `POST /api/chat`

## AI & RAG

- Knowledge base built from `backend/app/dummy_data.py`
- `backend/app/rag.py` uses LangChain + OpenAI embeddings + FAISS

## MySQL schema

- `mysql-schema.sql` includes users, destinations, packages, bookings, chatbot_logs, blogs.

## Deployment (AWS EC2 + Nginx)

1. Provision EC2 instance (Ubuntu 22.04).
2. Install Docker, Docker Compose, Nginx.
3. Clone repo and set environment variables.
4. Run `docker-compose up -d --build`.
5. Configure `nginx` reverse proxy to route frontend and backend.
6. Use Certbot to enable HTTPS.

## CI/CD

- Pipeline in `.github/workflows/ci-cd.yml`
- Build and deploy placeholders included

## Extra features implemented

- Wishlist + compare UI placeholders
- AI trip cost and itinerary from backend endpoint
- Floating chatbot widget for `Traveller Buddy`
- Multi-destination filters

