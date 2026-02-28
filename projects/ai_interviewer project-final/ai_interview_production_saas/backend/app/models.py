
from sqlalchemy import Column, Integer, Text, Boolean
from app.database import Base

class InterviewQA(Base):
    __tablename__ = "interview_qa"
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    silence = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, unique=True, index=True)
    hashed_password = Column(Text)
    is_admin = Column(Boolean, default=False)
