
from fastapi import FastAPI
from app.routes import interview

app = FastAPI(title="AI Interview SaaS")

app.include_router(interview.router, prefix="/api/interview")
