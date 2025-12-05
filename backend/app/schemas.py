from pydantic import BaseModel, EmailStr
from typing import Optional, Any, List
from datetime import datetime

class SignupPayload(BaseModel):
    email: EmailStr
    password: str
    event: Optional[str]

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    event: Optional[str]
    experience_level: Optional[str]
    goals: Optional[str]
    class Config:
        orm_mode = True

class WorkoutCreate(BaseModel):
    type: str
    metadata: dict
    notes: Optional[str] = None

class WorkoutOut(BaseModel):
    id: str
    user_id: str
    type: str
    metadata: dict
    notes: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True

