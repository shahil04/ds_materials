from pydantic import BaseModel

class TodoBase(BaseModel):
    serial_number: str
    title: str
    due_date: str
    due_time: str
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    pass

class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True
