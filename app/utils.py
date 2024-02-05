from fastapi import Depends
from passlib.context import CryptContext
from app import models
from .database import get_db
from app.database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"] ,deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)