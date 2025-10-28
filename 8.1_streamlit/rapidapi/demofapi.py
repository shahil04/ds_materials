from fastapi import FastAPI

# Create a FastAPI instance
app = FastAPI(title="My First API", version="1.0")

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to my first FastAPI app!"}

# Example endpoint with path parameter
@app.get("/hello/{name}")
def greet_user(name: str):
    return {"message": f"Hello, {name}! Welcome to FastAPI."}
