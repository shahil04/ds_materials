# First App
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Run the app:
# uvicorn main:app --reload
#
# Path Parameters
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

# Query Parameters
@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# Request Body with Pydantic
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str
    price: float

@app.post("/item")
def create_item(item: Item):
    return item
