from fastapi import APIRouter , Depends , HTTPException ,status
from sqlalchemy.orm import Session
from .. import models , database
from .. import schemas
from .. Oauth2 import get_current_user

router = APIRouter()

@router.post("/vote",status_code=status.HTTP_201_CREATED)
def vote(vote : schemas.Vote ,db : Session = Depends(database.get_db) ,\
                             current_user : dict = Depends(get_current_user)):
    
    get_post = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post = get_post.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                            detail=f"Post with id : {vote.post_id} do not exists")
    
    like_exists_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,models.Votes.user_id==current_user.id)
    like_exists = like_exists_query.first()
    if vote.vote_dir == 1:
        if like_exists :
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , \
                            detail="The Post is already voted by you")
        
        new_vote = models.Votes(post_id = vote.post_id , user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Your Vote been accepted"}
    else:
        if not like_exists:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , \
                            detail="No Vote Found")
        like_exists_query.delete()
        db.commit()
        return {"message":"Your Vote been deleted"}
    




    




