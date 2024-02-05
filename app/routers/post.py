from fastapi import APIRouter, Depends, HTTPException, Response, status
from app import models
from ..database import get_db
from sqlalchemy.orm import Session
from app.schema import CreatePost, PostSchema
import app.oauth2
from typing import Optional


router = APIRouter(
tags=['posts']
)

# get post for that logged in user
@router.get("/posts" , response_model=list[PostSchema])
def get_post(db: Session = Depends(get_db), 
            user_id : int= Depends(app.oauth2.get_current_user),
            limit: int = 3,
            skip : int = 0,
            search : Optional[str] = "" ):
       Id_from_token = user_id.id
       posts = db.query(models.PSchema).filter(models.PSchema.user_id == Id_from_token).filter(models.PSchema.title.like(f'%{search}%')).limit(limit).offset(skip).all()
       return posts


# get request (Specific)
@router.get("/posts/{id}", response_model=PostSchema)
def get_post_by_id(id: int, 
                   db : Session = Depends(get_db) 
                   ,user_id:int=Depends(app.oauth2.get_current_user)):
    posts = db.query(models.PSchema).filter(models.PSchema.id == id).first()
    if posts is None:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")
    
    return posts
    
#Create Post
from fastapi import Depends

@router.post("/postscreate", status_code=status.HTTP_201_CREATED, response_model=PostSchema)
def create_post(
    post: CreatePost,
    db: Session = Depends(get_db),
    user = Depends(app.oauth2.get_current_user)
):
    user_id = user.id
    new_post = models.PSchema(**post.dict(), user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



#update post
@router.put("/posts/update/{id}" ,response_model=PostSchema)
def update_post(id: int, 
                post_data: CreatePost,
                db: Session = Depends(get_db), 
                user_id : int= Depends(app.oauth2.get_current_user)):
    Id_from_token = user_id.id
    post = db.query(models.PSchema).filter(models.PSchema.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    if post.user_id != Id_from_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You Cannot Perform This Operation")
    post.title = post_data.title
    post.content = post_data.content
    db.commit()

    return post


#delete specific post
@router.delete("/posts/delete/{id}")
def delete_post(id: int,
                 db : Session = Depends(get_db), 
                user_id : int= Depends(app.oauth2.get_current_user)):
   Id_from_token = user_id.id
   post = db.query(models.PSchema).filter(models.PSchema.id == id)
   
   if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Index {id} is not a Valid Index")
   if post.user_id != Id_from_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You Cannot Perform This Operation")
   post.delete(synchronize_session=False)
   db.commit()
   return {Response(status_code=status.HTTP_204_NO_CONTENT), "Successfully Deleted Message"}
   

#delete data for that user
@router.delete("/clear")
def delete_data(db: Session = Depends(get_db), 
                user_id: int = Depends(app.oauth2.get_current_user)):
    Id_from_token = user_id.id
    post = db.query(models.PSchema).filter(models.PSchema.user_id == Id_from_token)
    deleted_rows = post.delete(synchronize_session=False)
    if deleted_rows == 0:
        raise HTTPException(status_code=404, detail="No data found for the user")
    db.commit()
    return {"message": "Data Deleted", "deleted_rows": deleted_rows}
