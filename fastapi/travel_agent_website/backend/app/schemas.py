from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class PackageBase(BaseModel):
    name: str
    destination: str
    duration_days: int
    price: float
    tags: Optional[str]
    description: Optional[str]
    image_url: Optional[str]

class PackageCreate(PackageBase):
    pass

class PackageRead(PackageBase):
    id: int

    class Config:
        orm_mode = True

class ItineraryRequest(BaseModel):
    destination: str
    days: int
    budget: float
    people: int

class ItineraryOutput(BaseModel):
    destination: str
    itinerary: List[dict]
    hotels: List[str]
    transport: List[str]
    estimated_cost: str
    tips: List[str]

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    destination: Optional[str]
    itinerary: Optional[List[dict]]
    hotels: Optional[List[str]]
    transport: Optional[List[str]]
    estimated_cost: Optional[str]
    tips: Optional[List[str]]
    answer: str

class BlogRead(BaseModel):
    id: int
    title: str
    category: str
    content: str
    publish_date: datetime

    class Config:
        orm_mode = True
