from pydantic import BaseModel, EmailStr
from typing import Optional



class PostBase(BaseModel):
    title: str
    body: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserCreateResp(BaseModel):
    id: int

class User(BaseModel):
    email: EmailStr

class Post(PostBase):
    id: int

class PostCreate(PostBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None