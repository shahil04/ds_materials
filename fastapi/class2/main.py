from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Student Portal API")

# In-memory student DB
students_db = []

# Pydantic models
class Student(BaseModel):
    id: int
    name: str
    age: int
    email: str
    course: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    course: Optional[str] = None

# ====================== STUDENT PORTAL ========================

@app.get("/student/{student_id}", tags=["Student Portal"])
def get_student_profile(student_id: int):
    for student in students_db:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.post("/student/register", tags=["Student Portal"])
def register_student(student: Student):
    for s in students_db:
        if s.id == student.id:
            raise HTTPException(status_code=400, detail="Student already exists")
    students_db.append(student)
    return {"message": "Student registered successfully", "data": student}

# ======================== ADMIN PORTAL ========================

@app.get("/admin/students", tags=["Admin Portal"])
def get_all_students():
    return students_db

@app.put("/admin/student/{student_id}", tags=["Admin Portal"])
def update_student(student_id: int, update: StudentUpdate):
    for student in students_db:
        if student.id == student_id:
            if update.name: student.name = update.name
            if update.age: student.age = update.age
            if update.email: student.email = update.email
            if update.course: student.course = update.course
            return {"message": "Student updated", "data": student}
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/admin/student/{student_id}", tags=["Admin Portal"])
def delete_student(student_id: int):
    for i, student in enumerate(students_db):
        if student.id == student_id:
            del students_db[i]
            return {"message": "Student deleted"}
    raise HTTPException(status_code=404, detail="Student not found")
