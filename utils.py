from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import schema
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import dbhelper as db
import settings

oauth2_schema = OAuth2PasswordBearer('/users/login/')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash(password): return pwd_context.hash(password)

def verify(plain_password, hashed_password): return pwd_context.verify(plain_password, hashed_password)


SECRET_KEY = settings.envvars.secret_key
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = settings.envvars.access_token_expire_mins
USER_ID_K = 'user_id'


def create_access_token(data:dict):
    d = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    d.update({'exp': expire})

    encoded_jwt = jwt.encode(d, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    token_data = None
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])

        id = payload.get(USER_ID_K)
        
        if not id:
            raise credentials_exception
        token_data = schema.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_schema)):
    credentials_except = HTTPException(status.HTTP_401_UNAUTHORIZED, 'invalid credentials', 
                                       {'WWW-Authenticate': 'Bearer'})
    token_data = verify_access_token(token, credentials_except)
    usr = db.get_user(token_data.id)
    return usr 