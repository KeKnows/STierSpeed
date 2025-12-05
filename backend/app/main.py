from fastapi import FastAPI, HTTPException, Depends, Header
from app.schemas import SignupPayload, LoginPayload, UserOut, WorkoutCreate, WorkoutOut
from app import crud
from app.auth import create_access_token, decode_token
from app.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.ai_client import build_summary_prompt, call_ai_summary

# create DB tables (for demo / init). In production run Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="StierSpeed")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    token = authorization.split("Bearer ")[-1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    # crud functions use DB
    user = crud.get_user_by_id(user_id) if hasattr(crud, "get_user_by_id") else None
    # fallback: our create_access_token includes email or user id; but below we'll use subject as id
    # For simplicity we'll return payload (id + email)
    return payload

@app.post("/signup", status_code=201)
def signup(p: SignupPayload):
    try:
        user = crud.create_user(p.email, p.password, event=p.event)
        return {"id": user.id, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail="User already exists or invalid data")

@app.post("/login")
def login(payload: LoginPayload):
    user = crud.authenticate_user(payload.email, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.id, "email": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/workouts", response_model=WorkoutOut)
def create_workout(workout: WorkoutCreate, authorization: str = Header(None)):
    token = authorization.split("Bearer ")[-1] if authorization else None
    payload = decode_token(token) if token else None
    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = payload.get("sub")
    w = crud.create_workout(user_id, workout.type, workout.metadata, workout.notes)
    return w

@app.get("/workouts", response_model=list[WorkoutOut])
def list_workouts(authorization: str = Header(None)):
    token = authorization.split("Bearer ")[-1] if authorization else None
    payload = decode_token(token) if token else None
    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = payload.get("sub")
    rows = crud.list_workouts(user_id)
    return rows

@app.get("/ai/weekly-summary")
async def weekly_summary(authorization: str = Header(None)):
    token = authorization.split("Bearer ")[-1] if authorization else None
    payload = decode_token(token) if token else None
    if not payload:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = payload.get("sub")
    # gather last 7 workouts
    workouts = [w.__dict__ for w in crud.list_workouts(user_id, limit=50)]
    user_profile = {"id": user_id}
    prompt = build_summary_prompt(user_profile, workouts)
    summary = await call_ai_summary(prompt)
    return {"summary": summary}

