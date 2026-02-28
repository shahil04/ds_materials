
from sqlalchemy import Column, Integer, String, Text, Boolean
from app.database import Base

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True)
    question = Column(Text)
    answer = Column(Text)
    silence = Column(Boolean)
