from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from schema import Post, PostCreate, UserCreate
from typing import Optional
import dbhelper as db
from routers import posts, users



app = FastAPI()
db.setup()



@app.get('/')
async def root():
    return { 'message': 'hello!!' }


app.include_router(posts.router)
app.include_router(users.router)
