from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    current_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    if current_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id: {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
   
    if found_vote:
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"You have removed your like from this post"}
    else:
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added vote"}
