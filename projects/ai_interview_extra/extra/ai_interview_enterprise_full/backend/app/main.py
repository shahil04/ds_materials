
from fastapi import FastAPI
from app.database import Base, engine
from app.routes import interview, dashboard

Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Enterprise AI Interview SaaS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview.router, prefix="/api/interview")
app.include_router(dashboard.router, prefix="/api/dashboard")
