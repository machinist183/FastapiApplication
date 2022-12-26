from fastapi import APIRouter,status,HTTPException,Depends,Response
from typing import Optional , List
from .. import models
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..Oauth2 import get_current_user

router = APIRouter(
    prefix="/posts"
)

def get_number_of_votes(post_id : int,db):
    vote_count = len(db.query(models.Votes).filter(models.Votes.post_id == post_id).all())
    return vote_count

@router.get("/")
def home(db: Session = Depends(get_db),user :str = Depends(get_current_user) ,limit:int = 10 , skip:int = 0,search:Optional[str] =""):
    # cursor.execute("""SELECT * FROM "Posts";""")
    # posts  = cursor.fetchall()
    request = db.query(models.Post ,func.count(models.Votes.post_id).label('Votes')).\
                join(models.Votes , models.Post.id == models.Votes.post_id , isouter = True)\
                .filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limit).offset(skip).all()
    return request


@router.post("/" , status_code = status.HTTP_201_CREATED , response_model=schemas.PostResponse )
def create_post(post: schemas.CreatePost ,db: Session = Depends(get_db),user :str = Depends(get_current_user)):
    # cursor.execute("""INSERT INTO "Posts" (title , content , published , rating) VALUES(%s , %s,%s ,%s) RETURNING *""",
    #                     (post.title , post.content , post.published ,post.rating))
    # post = cursor.fetchone()
    # conn.commit()
    print(user.id)
    new_post = models.Post(owner_id = user.id , **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}" )
def get_one_post(id : int,db: Session = Depends(get_db),user :str = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM "Posts" WHERE id= %s""",(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"message : No post with id {id} found")
    request = db.query(models.Post ,func.count(models.Votes.post_id).label('Votes')).\
                join(models.Votes , models.Post.id == models.Votes.post_id , isouter = True)\
                    .filter(models.Post.id == id).group_by(models.Post.id).all()
    return request

@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int ,db: Session = Depends(get_db),user :str = Depends(get_current_user)):
    # cursor.execute("""DELETE FROM "Posts" WHERE id  = %s RETURNING *""",(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    get_post = db.query(models.Post).filter(models.Post.id == id)
    post = get_post.first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , \
                            detail=f"The post with id {id} do no exists")
    if user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,\
                            detail="Youre not authorised to do this")
    get_post.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}" , status_code=status.HTTP_205_RESET_CONTENT,response_model=schemas.PostResponse)
def update_post(id : int , updated_post : schemas.UpdatePost ,db: Session = Depends(get_db),user :str = Depends(get_current_user)):
    # cursor.execute("""UPDATE "Posts" SET title = %s , content = %s , published= %s , rating = %s \
    #                     WHERE id = %s RETURNING *""",(post.title , post.content , post.published , post.rating , str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    get_post = db.query(models.Post).filter(models.Post.id == id)
    post = get_post.first()
    if post == None : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , \
                            detail=f"The post with id {id} do no exists")
    if user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,\
                            detail="Youre not authorised to do this")
    get_post.update(updated_post.dict())
    db.commit()
    return get_post.first()
