
from fastapi import APIRouter
router = APIRouter()

@router.post("/start")
def start(job_role: str):
    return {"status": "started", "job_role": job_role}

@router.post("/reply")
def reply(answer: str):
    return {"ai": "Tell me more about your experience."}

@router.post("/grade")
def grade():
    return {"score": 8, "verdict": "Hire"}
