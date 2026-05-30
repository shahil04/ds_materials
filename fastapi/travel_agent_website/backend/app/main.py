import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from . import models, schemas, crud
from .database import engine, get_db
from .auth import create_access_token, decode_access_token, authenticate_user
from .config import settings
from .rag import rag_response, build_knowledge_base

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    # Build initial knowledge base on startup if missing
    from .dummy_data import knowledge_docs

    if not os.path.exists("rag_store.faiss"):
        build_knowledge_base(knowledge_docs())

@app.post("/api/auth/register", response_model=schemas.UserRead)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already in use")
    created = await crud.create_user(db, user)
    return created

@app.post("/api/auth/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/packages", response_model=List[schemas.PackageRead])
async def get_packages(
    destination: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_days: Optional[int] = None,
    max_days: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
):
    return await crud.list_packages(db, destination, min_price, max_price, min_days, max_days)

@app.post("/api/packages", response_model=schemas.PackageRead)
async def create_package(package: schemas.PackageCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_package(db, package)

@app.put("/api/packages/{package_id}", response_model=schemas.PackageRead)
async def update_package(package_id: int, package: schemas.PackageCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_package(db, package_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Package not found")
    return await crud.update_package(db, package_id, package)

@app.delete("/api/packages/{package_id}")
async def delete_package(package_id: int, db: AsyncSession = Depends(get_db)):
    existing = await crud.get_package(db, package_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Package not found")
    await crud.delete_package(db, package_id)
    return {"message": "Deleted"}

@app.post("/api/generate-itinerary", response_model=schemas.ItineraryOutput)
async def generate_itinerary(request: schemas.ItineraryRequest):
    # deterministic dummy output based on request
    day_plans = []
    activities = ["Beach", "City Tour", "Local Market", "Adventure", "Relax", "Cultural Experience", "Water Sports", "Spa"]
    for i in range(1, request.days + 1):
        plan = f"Day {i}: {activities[(i - 1) % len(activities)]} in {request.destination}."
        day_plans.append({"day": i, "plan": plan})

    est_cost = int((request.budget * request.people) * 0.95)
    return {
        "destination": request.destination,
        "itinerary": day_plans,
        "hotels": [f"{request.destination} Grand Hotel", f"{request.destination} Premier Resort"],
        "transport": ["Flight", "Local Taxi", "Shuttle"],
        "estimated_cost": f"₹{est_cost:,}",
        "tips": ["Avoid peak season.", "Book early for best deals.", "Carry local cash."]
    }

@app.post("/api/chat", response_model=schemas.ChatResponse)
async def chat(request: schemas.ChatRequest):
    llm_answer = rag_response(request.query)
    return schemas.ChatResponse(
        destination=None,
        itinerary=None,
        hotels=None,
        transport=None,
        estimated_cost=None,
        tips=None,
        answer=llm_answer,
    )
