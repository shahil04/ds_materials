
from fastapi import APIRouter

router = APIRouter()

@router.get("/stats")
def stats():
    return {
        "total_interviews": 8,
        "avg_score": 7.2,
        "hire_rate": "55%"
    }
