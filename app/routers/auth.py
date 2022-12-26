from fastapi import APIRouter , Response ,status,Depends ,HTTPException
from ..database import get_db
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models , Oauth2
from .. import schemas
from ..utils import verify_pass

router = APIRouter()

@router.post("/login" ,response_model=schemas.TokenData)
def userLogin(user_info : OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_info.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , \
                            detail=f"hey Invalid Credentials")
    if not verify_pass(user_info.password , user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN ,detail="Invalid Credentials")
    token = Oauth2.create_jwt_token({"user_id":user.id , "email":user.email})
    return {"generated_token": token , "token_type":"bearer"}


    