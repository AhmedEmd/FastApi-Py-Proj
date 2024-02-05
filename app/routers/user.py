
from fastapi import  APIRouter, Depends, HTTPException, status
from app import models, utils
from app.database import get_db
from sqlalchemy.orm import Session
from app.schema import Usercreate, Useresponse


router = APIRouter(
    tags=['Create Users']
)


#sign up 
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=Useresponse)
def Sign_up(detail: Usercreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(detail.password)
    detail.password = hashed_password
    details = models.User(**detail.dict())
    db.add(details)
    db.commit()
    db.refresh(details)
    return details


@router.get("/viewprofile/{id}", status_code=status.HTTP_200_OK, response_model=Useresponse)
def get_user(id: int, db: Session = Depends(get_db)):
    data = db.query(models.User).filter(models.User.id == id).first()
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with the id of {id} is not found"
        )
    return data

