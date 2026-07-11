# app/features/users/user_models.py
from sqlalchemy import Column, Integer, String
from app.config.database import Base
from pydantic import BaseModel, EmailStr

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=True, index=True)
    role = Column(String, index=True)
