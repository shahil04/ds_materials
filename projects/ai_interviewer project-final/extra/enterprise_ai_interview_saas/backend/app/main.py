
from fastapi import FastAPI
from app.core.database import Base, engine
from app.routes import auth, interview, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise AI Interview SaaS")

app.include_router(auth.router, prefix="/api/auth")
app.include_router(interview.router, prefix="/api/interview")
app.include_router(admin.router, prefix="/api/admin")
