
from sqlalchemy import Column, Integer, Text, Boolean
from app.database import Base

class InterviewQA(Base):
    __tablename__ = "interview_qa"
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    silence = Column(Boolean, default=False)
