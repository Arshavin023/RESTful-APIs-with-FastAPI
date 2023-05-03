from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic.types import conint #this help define schema to be 1 or 0

# Schema of input from user to create and update a post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass 
 
 # Schema for input from user to create an account
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Schema for response after successful account creation
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config: #this tells pydantic model to convert alchemy model to be a pydantic model
        orm_mode=True

# Schema for response after successful post creation
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse

    class Config: #this tells pydantic model to convert alchemy model to be a pydantic model
        orm_mode=True

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse
    class Config: #this tells pydantic model to convert alchemy model to be a pydantic model
        orm_mode=True


class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config: #this tells pydantic model to convert alchemy model to be a pydantic model
        orm_mode = True

# Schema for input from existing user while logging in
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Schema for token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


# Schema for retrieving number of posts for a user

class User(UserResponse):
    class Config: #this tells pydantic model to convert alchemy model to be a pydantic model
        orm_mode = True

class UserPostOut(BaseModel):
    User: User
    posts: int
    class Config: #this tells pydantic model to convert alchemy model to be a pydantic model
        orm_mode = True

