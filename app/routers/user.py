from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, utils, oauth2
from ..database import get_db

router=APIRouter(
    prefix="/users", # replace /users with / or /{id} in routers below
    tags=["Users"]
)

# Route for create a user 
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db: Session=Depends(get_db)):
    # has the passowrd 
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user=models.User(**user.dict()) #unpack post request from user and stores in different fields for the database
    
    user_check = db.query(models.User).filter(models.User.email == new_user.email).first()

    if user_check: #check if user already exists in the system and throw error is yes
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='Email already registered')
    db.add(new_user) #add the post to the database
    db.commit() # commit changes to the database
    db.refresh(new_user) #refresh the database to return the new post  
    return new_user

# Get a user info with id
@router.get('/{id}',response_model=schemas.UserResponse)
def get_user(id: int,db: Session=Depends(get_db),
             user_id: int=Depends(oauth2.get_current_user)
             ):
    # check to see if user exists
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} does not exists')
    return user


