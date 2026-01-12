
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import interview,resume

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Interview Production SaaS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview.router, prefix="/api/interview")

app.include_router(resume.router, prefix="/api/resume")
