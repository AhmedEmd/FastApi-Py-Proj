from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .utils import verify
from .oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.schema import Token
router = APIRouter(
    tags=['authentication']
)

@router.post("/login", response_model=Token)
def login(auth: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):

    #oauth shit takes the reqest and stores it in username and password form so change email
    #to user name

    user = db.query(User).filter(User.email == auth.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User Doesn't exist")
    if not verify(auth.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User Doesn't exist")
    access_token =  create_access_token(data = {"user_id" : user.id})
    return {"access_token" : access_token, "token_type" : "bearer"}