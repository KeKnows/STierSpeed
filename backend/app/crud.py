from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models import User, Workout
from app.auth import hash_password, verify_password
from app.db import SessionLocal

def create_user(email: str, password: str, event: str = None):
    db = SessionLocal()
    try:
        user = User(email=email, password_hash=hash_password(password), event=event)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise
    finally:
        db.close()

def authenticate_user(email: str, password: str):
    db = SessionLocal()
    try:
        stmt = select(User).where(User.email == email)
        user = db.execute(stmt).scalar_one_or_none()
        if user and verify_password(password, user.password_hash):
            return user
        return None
    finally:
        db.close()

def create_workout(user_id: str, type_: str, metadata: dict, notes: str = None):
    db = SessionLocal()
    try:
        w = Workout(user_id=user_id, type=type_, metadata=metadata, notes=notes)
        db.add(w)
        db.commit()
        db.refresh(w)
        return w
    finally:
        db.close()

def list_workouts(user_id: str, limit: int = 100):
    db = SessionLocal()
    try:
        stmt = select(Workout).where(Workout.user_id == user_id).order_by(Workout.created_at.desc()).limit(limit)
        rows = db.execute(stmt).scalars().all()
        return rows
    finally:
        db.close()

def get_workout_by_id(workout_id: str):
    db = SessionLocal()
    try:
        stmt = select(Workout).where(Workout.id == workout_id)
        return db.execute(stmt).scalar_one_or_none()
    finally:
        db.close()

def delete_workout(workout_id: str):
    db = SessionLocal()
    try:
        w = get_workout_by_id(workout_id)
        if w:
            db.delete(w)
            db.commit()
            return True
        return False
    finally:
        db.close()

def get_user_by_id(user_id: str):
    db = SessionLocal()
    try:
        stmt = select(User).where(User.id == user_id)
        return db.execute(stmt).scalar_one_or_none()
    finally:
        db.close()
