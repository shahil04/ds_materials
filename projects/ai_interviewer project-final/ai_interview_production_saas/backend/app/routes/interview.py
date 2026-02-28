from fastapi import APIRouter

router = APIRouter()

QUESTIONS = [
    "Introduce yourself",
    "Explain your last project",
    "What is Python?",
    "Explain SQL joins",
    "What is REST API?",
    "Explain Docker",
    "Explain system design",
    "Do you have any questions for us?"
]

current_index = 0

@router.get("/next")
def next_question():
    global current_index

    if current_index >= len(QUESTIONS):
        return {"done": True}

    question = QUESTIONS[current_index]
    current_index += 1

    return {
        "done": False,
        "text": question
    }




# from fastapi import APIRouter
# from app.database import SessionLocal
# from app.models import InterviewQA

# router = APIRouter()

# QUESTIONS = [
#     "Introduce yourself",
#     "Explain your last project",
#     "What is Pyathon?",
#     "Explain SQL joins",
#     "What is REST API?",
#     "Explain Docker",
#     "Explain system design",
#     "Any questions for us?"
# ]

# index = 0

# @router.get("/next")
# def next_question():
#     global index
#     if index >= len(QUESTIONS):
#         return {"done": True}
#     q = QUESTIONS[index]
#     index += 1
#     return {"text": q}

# @router.post("/answer")
# def save_answer(question: str, answer: str, silence: bool = False):
#     db = SessionLocal()
#     db.add(InterviewQA(question=question, answer=answer, silence=silence))
#     db.commit()
#     return {"status": "saved"}
