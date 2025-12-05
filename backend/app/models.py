from sqlalchemy import Column, String, DateTime, JSON, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db import Base

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    event = Column(String)
    experience_level = Column(String)
    goals = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=text('now()'))

    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String, nullable=False)   # 'sprint' or 'strength'
    metadata = Column(JSON)
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=text('now()'))

    user = relationship("User", back_populates="workouts")

