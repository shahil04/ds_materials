
from fastapi import APIRouter
router = APIRouter()

@router.get("/dashboard")
def dashboard():
    return {"total_interviews": 12, "hires": 7}
