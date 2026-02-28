
from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True)
    job_role = Column(String)
    transcript = Column(Text)
    scorecard = Column(Text)
