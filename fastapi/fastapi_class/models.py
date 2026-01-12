from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    serial_number = Column(String)
    title = Column(String, index=True)
    due_date = Column(String)
    due_time = Column(String)
    completed = Column(Boolean, default=False)
