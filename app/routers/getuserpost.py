from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/totalposts", #replace /posts with / or /{id} in different routes below
    tags=["Total Posts"]
)
# retrieve all posts with ORM or SQL Alchemy
# @router.get("/",response_model=List[schemas.PostResponse])
@router.get("/",response_model=List[schemas.UserPostOut])
def get_posts(db: Session=Depends(get_db),
              current_user: int=Depends(oauth2.get_current_user),
              limit: int = 10,skip: int = 0,
              search: Optional[str] = ""):
    

    # Performing left outer join, group by and count 
    # posts = db.query(models.User, func.count(models.Post.id).label("posts")).join(
    #     models.Post, models.Post.user_id==models.User.id,isouter=True).group_by(models.User.id) \
    # .filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.User, func.count(models.Post.id).label("posts")).join(
        models.Post, models.Post.user_id==models.User.id,isouter=True).group_by(models.User.id) \
    .filter(models.Post.title.contains(search)) \
        .order_by(func.count(models.Post.id).desc()) \
            .limit(limit).offset(skip).all()

    #To ensure the current logged user retrieves only his his posts
    # posts=db.query(models.Post).filter(models.Post.user_id == current_user.id).all()

    return posts


# Retrieve a particular post
@router.get("/{id}",response_model=schemas.UserPostOut)
def get_post(id:int, db: Session=Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):

    # To retrieve number of posts for a particular user

    # Performing left outer join, group by and count 
    post = db.query(models.User, func.count(models.Post.id).label("posts")).join(
        models.Post, models.Post.user_id==models.User.id,isouter=True).group_by(models.User.id) \
        .filter(models.User.id == id).first()
    
    # post = db.query(models.Post).filter(models.Post.user_id == id).all()
    
    # if no result was returned then it means user doesn't exist
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id: {id} was not found')


    return post
