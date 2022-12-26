from pydantic import BaseModel ,EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint

#schema for User
#--->Request
class getUser(BaseModel):
    email : EmailStr
    password : str

#--->Response
class userOut(BaseModel):
    id : int
    email : str
    createdAt : datetime

    class Config:
        orm_mode = True


#schema for posts#
#--->Request
class BasePost(BaseModel):
    title : str
    content : str
class CreatePost(BasePost):
    rating : Optional[int] = 0
    published : Optional[bool] = False
class UpdatePost(CreatePost):
    pass

#--->Response
class PostResponse(BasePost):
    id:int
    createdAt : datetime
    owner_id : int
    owner : userOut
    class Config:
        orm_mode = True

    
   


#token schemas
class TokenData(BaseModel):
    generated_token : str
    token_type : str
    class Config:
        orm_mode = True

class TokenPayLoad(BaseModel):
    id : Optional[int] 
    email : str

#Voting Schema
class Vote(BaseModel):
    post_id : int
    vote_dir : conint(le=1)