from jose import JWTError, jwt
from datetime import datetime , timedelta
from fastapi import HTTPException , Depends ,status 
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from . import models
from .config import settings

Oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithms
ACCESS_TOKEN_EXPIRE_MINUTES = settings.token_expirE_time

def create_jwt_token(payLoad : dict):
    to_encode = payLoad.copy()
    expiry = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expiry})
    token = jwt.encode(to_encode , SECRET_KEY , algorithm=ALGORITHM)
    return token

def verify_jwt_token(token : str ,credentials_exception):
    try:
        payLoad = jwt.decode(token, SECRET_KEY ,algorithms=[ALGORITHM])
        email= payLoad.get("email")
        if not email:
            raise credentials_exception
        return email
    except JWTError:
        raise credentials_exception

def get_current_user(token : str = Depends(Oauth2_scheme), db:Session =  Depends(get_db)):
    credenital_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED ,\
                                         detail=f"Invalid Token")
    email = verify_jwt_token(token , credentials_exception=credenital_exception)
    user = db.query(models.User).filter(models.User.email == email).first()
    return user





