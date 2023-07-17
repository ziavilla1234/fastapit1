from fastapi import FastAPI, Response, status, HTTPException, APIRouter, Depends
from schema import Post, PostCreate, UserCreate
import dbhelper as db
import utils as utls

router = APIRouter(prefix='/posts', tags=['posts'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, curr_usr: int = Depends(utls.get_current_user)):
    
    res = db.new_post(post.title, post.body)
    
    if type(res) is str:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res)

    return res

@router.get('/')
def get_posts():
    return db.get_posts()

@router.get('/{id}')
def get_post(id:int):
    pst = db.get_post(id)
    if not pst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')
    return pst

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    res = db.delete_post(id)
    if not res:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{int}')
def update_post(id:int, post:PostCreate):
    pst = db.update_post(id, post.title, post.body)

    if not pst:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} not found')
    
    return pst