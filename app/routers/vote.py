from fastapi import  APIRouter, Depends, HTTPException, status
from app import models
import app.oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from app.schema import VoteSchema



router = APIRouter(
    tags=['Voting']
)


@router.post("/vote", status_code=status.HTTP_201_CREATED)
def user_vote(
    vote: VoteSchema,
    db: Session = Depends(get_db),
    user_id: int = Depends(app.oauth2.get_current_user),
):
    current_user = user_id.id

    is_post_there = db.query(models.PSchema).filter(models.PSchema.id == vote.post_id).first()
    if not is_post_there:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Valid")
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user
    )
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user} has already voted for the post with the id of {vote.post_id}"
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user)
        db.add(new_vote)
        db.commit()
        return "Vote Added Successfully"
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="post already not voted"
            )

        vote_query.delete(synchronize_session=False)
        db.commit()
        return "Successfully Deleted Vote"


  
           


