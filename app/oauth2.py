from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends , status, HTTPException
from app import schema
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
import app.models
from app.configuration import settings

from app import models
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_JWT = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_JWT


def verify_access_token(token :str, credentials_exception):

    try:
     payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
     id = str(payload.get("user_id"))
     if id is None:
        raise credentials_exception
     token_data = schema.TokenData(id=id)
    except JWTError:
       raise credentials_exception
    
    return token_data
    


def get_current_user(token: str = Depends(oauth2_schema), db : Session = Depends(get_db) ):
   credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail=f"Invalid Credentials", 
                                         headers={"WWW-Authenticate": "Bearer"})
   result = verify_access_token(token , credentials_exception)
   User = db.query(app.models.User).filter(app.models.User.id == result.id).first()
   return result
   