from fastapi import APIRouter,status,HTTPException,Depends,Response
from typing import Optional , List
from .. import models
from .. import schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..utils import hash_pass

router = APIRouter(
    prefix="/users"
)

@router.post("/" ,status_code=status.HTTP_201_CREATED, response_model=schemas.userOut)
def UserLogin(user : schemas.getUser ,db: Session = Depends(get_db)):
    existing_User = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_User:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="Email Already Taken")
    user.password = hash_pass(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}" ,status_code=status.HTTP_201_CREATED, response_model=schemas.userOut)
def GetUser(id :int , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,\
                             detail=f"User with id {id} not found !!")
    return user
