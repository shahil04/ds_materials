
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class InterviewInit(BaseModel):
    job_role: str
    resume_text: str

@router.post("/init")
def init_interview(data: InterviewInit):
    return {"status": "initialized", "job_role": data.job_role}

@router.post("/reply")
def reply(text: str):
    return {"ai_response": "Tell me more about your experience."}

@router.post("/grade")
def grade():
    return {
        "score": 7,
        "verdict": "Hire"
    }
