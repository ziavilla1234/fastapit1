from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from schema import Post, PostCreate, UserCreate, Token, User, UserCreateResp
import dbhelper as db
import utils as utl

router = APIRouter(prefix='/users', tags=['users'])

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserCreateResp)
def create_user(user: UserCreate):
    usr = db.new_user(user.email, user.password)
    
    if type(usr) is str:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=usr)
    
    return {'id': usr[0], 'email':usr[1], 'password':usr[2]}

@router.get('/{id}', response_model=User)
def get_user(id:int):
    usr = db.get_user(id)
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} not found')
    return {'id': usr[0], 'email':usr[1], 'password':usr[2]}


@router.post('/login/', status_code=status.HTTP_201_CREATED, response_model=Token)
def login_user(user: OAuth2PasswordRequestForm = Depends()):

    usr = db.get_user_by_email(user.username)
    if not usr:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user not found')
    
    if not utl.verify(user.password, usr[2]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='user not found')
    
    access_token = utl.create_access_token({utl.USER_ID_K:usr[0]})
    return {'access_token': access_token, 'token_type': 'bearer'} 